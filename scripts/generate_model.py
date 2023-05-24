#!/usr/bin/env python3

"""
Generate the model.sdf file by substituting strings of the form "@foo" with calculated
values & configs obtained from a YAML configuration file.

The YAML configuration file requires the following fields:
    - model_name: The name of the model. This is used to specify the topics over
        which the thruster commands should be published.
    - mass: The mass of the vehicle.
    - control_method: The control method to use; 0 for thrust, 1 for velocity.
    - bounding_box: The bounding box of the vehicle. This is used to
        calculate the buoyancy and quadratic drag (if not provided).
    - center_of_mass: The center of mass of the vehicle.
    - center_of_volume: The center of volume of the vehicle.
    - buoyancy_adjustment: The amount of mass to add to the vehicle's mass when
        calculating the total displaced mass. This is used to adjust the buoyancy of
        the vehicle.
    - thrusters: A list of thruster locations on the vehicle provided in order of
        their declaration in the provided SDF file. Note that the thruster
        orientation should be configured in the SDF file.

In addition to the required fields, the following optional fields may be provided:
    - inertia: The inertia of the vehicle.
    - drag_coefficients: The drag coefficients of the vehicle (both linear and
        quadratic). If not provided, these will be calculated using the bounding
        box.
    - added_mass_coefficients: The added mass of the vehicle.
    - default_current: The velocity of the ocean current.

The SDF file uses the ArduPilotPlugin COMMAND control method; this sends commands to a
specified ign-transport topic rather than directly controlling a joint.

We use the COMMAND method to send commands to the Gazebo ThrusterPlugin. The
ThrusterPlugin supports 2 control methods:
      control thrust via /cmd_thrust
      control angular velocity via /cmd_vel

The ThrusterPlugin uses the Fossen equation to relate thrust to angular velocity, and
will apply thrust force to the joint and spin the propeller. Propellers have bounding
boxes and inertia, so spinning the propeller does affect the simulation.
"""

import math
import re
from argparse import ArgumentParser

import yaml

# SDF 1.9 supports degrees="true"; provide some nice vars for earlier versions
d180 = math.pi
d90 = d180 / 2
d45 = d90 / 2
d30 = d90 / 3
d135 = d90 + d45

# Density of water
fluid_density = 1000.0


def thrust_to_ang_vel(
    thrust: float,
    propeller_diameter: float,
    thrust_coefficient: float,
    fluid_density: float = 998,
) -> float:
    """Convert thrust to angular velocity.

    This is defined by Fossen in "Guidance and Control of Ocean Vehicles" on p. 246.

    Args:
        thrust: The thrust to convert to angular velocity.
        propeller_diameter: The diameter of the thruster's propeller.
        thrust_coefficient: The thrust coefficient of the thruster.
        fluid_density: The density of the fluid the ROV is moving in. Defaults to
            998 (density of water).

    Returns:
        Thrust converted to angular velocity.
    """
    assert thrust >= 0
    assert thrust_coefficient >= 0
    return math.sqrt(
        thrust / (fluid_density * thrust_coefficient * pow(propeller_diameter, 4))
    )


class ModelParams:
    """Wrapper for the parameters needed to generate an SDF for use by Gazebo."""

    def __init__(
        self,
        model_name: str,
        mass: float,
        collision: tuple[float, float, float],
        center_of_mass: tuple[float, float, float],
        center_of_volume: tuple[float, float, float],
        inertia: tuple[float, float, float],
        linear_drag: tuple[float, float, float, float, float, float],
        quadratic_drag: tuple[float, float, float, float, float, float],
        added_mass: tuple[float, float, float, float, float, float],
        default_current: tuple[float, float, float],
        thrusters: list[tuple[float, float, float]],
        use_angvel_cmd: int,
        propeller_size: str = "0.1 0.02 0.01",
        propeller_mass: float = 0.002,
        propeller_inertia: tuple[float, float, float] = (0.001, 0.001, 0.001),
        propeller_diameter: float = 0.1,
        thrust_coefficient: float = 0.02,
        max_thrust: float = 50,
        servo_range: tuple[float, float] = (1100, 1900),
        control_offset: float = -0.5,
    ) -> None:
        self.model_name = f'"{model_name}"'
        self.mass = mass

        # The collision box is used by the BuoyancyPlugin
        self.collision_x = collision[0]
        self.collision_y = collision[1]
        self.collision_z = collision[2]

        self.center_of_mass_x = center_of_mass[0]
        self.center_of_mass_y = center_of_mass[1]
        self.center_of_mass_z = center_of_mass[2]

        self.center_of_volume_x = center_of_volume[0]
        self.center_of_volume_y = center_of_volume[1]
        self.center_of_volume_z = center_of_volume[2]

        self.ixx = inertia[0]
        self.iyy = inertia[1]
        self.izz = inertia[2]

        self.xU = linear_drag[0]
        self.yV = linear_drag[1]
        self.zW = linear_drag[2]
        self.kP = linear_drag[3]
        self.mQ = linear_drag[4]
        self.nR = linear_drag[5]

        self.xUabsU = quadratic_drag[0]
        self.yVabsV = quadratic_drag[1]
        self.zWabsW = quadratic_drag[2]
        self.kPabsP = quadratic_drag[3]
        self.mQabsQ = quadratic_drag[4]
        self.nRabsR = quadratic_drag[5]

        self.xDotU = added_mass[0]
        self.yDotV = added_mass[1]
        self.zDotW = added_mass[2]
        self.kDotP = added_mass[3]
        self.mDotQ = added_mass[4]
        self.nDotR = added_mass[5]

        # The ocean current defaults to zero in Gazebo, but sometimes we want to test
        # our systems in a current.
        self.default_current_x = default_current[0]
        self.default_current_y = default_current[1]
        self.default_current_z = default_current[2]

        self.use_angvel_cmd = bool(use_angvel_cmd)

        # Propeller link parameters
        self.propeller_size = propeller_size
        self.propeller_mass = propeller_mass
        self.propeller_ixx = propeller_inertia[0]
        self.propeller_iyy = propeller_inertia[1]
        self.propeller_izz = propeller_inertia[2]

        # ThrusterPlugin parameters
        self.propeller_diameter = propeller_diameter
        self.thrust_coefficient = thrust_coefficient

        # ArduPilotPlugin control parameters
        self.servo_min = servo_range[0]
        self.servo_max = servo_range[1]
        self.control_offset = control_offset

        # Configure each thruster location and topic
        if use_angvel_cmd:
            self.cw_control_multiplier = (
                -thrust_to_ang_vel(max_thrust, propeller_diameter, thrust_coefficient)
                * 2
            )
            self.ccw_control_multiplier = (
                thrust_to_ang_vel(max_thrust, propeller_diameter, thrust_coefficient)
                * 2
            )
        else:
            self.cw_control_multiplier = max_thrust * 2
            self.ccw_control_multiplier = max_thrust * 2

        for i, thruster in enumerate(thrusters):
            thruster_num = i + 1

            setattr(self, f"thruster{thruster_num}_x", thruster[0])
            setattr(self, f"thruster{thruster_num}_y", thruster[1])
            setattr(self, f"thruster{thruster_num}_z", thruster[2])

            topic = f"/model/{model_name}/joint/thruster{thruster_num}_joint/cmd_"

            if use_angvel_cmd:
                topic += "vel"
            else:
                topic += "thrust"

            setattr(self, f"thruster{thruster_num}_topic", topic)


def get_model_params_from_config(config_path: str) -> ModelParams:
    """Generate a model from a YAML config file.

    Args:
        config_path: The full path to the configuration file to load.

    Returns:
        A ModelParams object containing the vehicle's parameters.
    """
    with open(config_path) as config_file:
        config = yaml.safe_load(config_file)

        mass = config["mass"]

        bounding_x = config["bounding_box"]["x"]
        bounding_y = config["bounding_box"]["y"]
        bounding_z = config["bounding_box"]["z"]

        displaced_mass = mass + config["buoyancy_adjustment"]

        collision = (
            bounding_x,
            bounding_y,
            displaced_mass / (bounding_x * bounding_y * fluid_density),
        )

        try:
            inertia = (
                config["inertia"]["ixx"],
                config["inertia"]["iyy"],
                config["inertia"]["izz"],
            )
        except KeyError:
            ixx = mass / 12 * (collision[1] ** 2 + collision[2] ** 2)
            iyy = mass / 12 * (collision[0] ** 2 + collision[2] ** 2)
            izz = mass / 12 * (collision[0] ** 2 + collision[1] ** 2)
            inertia = (ixx, iyy, izz)

        try:
            linear_drag = (
                config["linear_drag"]["xU"],
                config["linear_drag"]["yV"],
                config["linear_drag"]["zW"],
                config["linear_drag"]["kP"],
                config["linear_drag"]["mQ"],
                config["linear_drag"]["nR"],
            )
        except KeyError:
            linear_drag = (0, 0, 0, 0, 0, 0)

        try:
            quadratic_drag = (
                config["quadratic_drag"]["xUabsU"],
                config["quadratic_drag"]["yVabsV"],
                config["quadratic_drag"]["zWabsW"],
                config["quadratic_drag"]["kPabsP"],
                config["quadratic_drag"]["mQabsQ"],
                config["quadratic_drag"]["nRabsR"],
            )
        except KeyError:
            xUabsU = -0.5 * bounding_y * bounding_z * 0.8 * fluid_density
            yVabsV = -0.5 * bounding_x * bounding_z * 0.95 * fluid_density
            zWabsW = -0.5 * bounding_x * bounding_y * 0.95 * fluid_density
            kPabsP = -0.5 * 0.008 * fluid_density
            mQabsQ = -0.5 * 0.008 * fluid_density
            nRabsR = -0.5 * 0.008 * fluid_density

            quadratic_drag = (xUabsU, yVabsV, zWabsW, kPabsP, mQabsQ, nRabsR)

        try:
            added_mass = (
                config["added_mass"]["xDotU"],
                config["added_mass"]["yDotV"],
                config["added_mass"]["zDotW"],
                config["added_mass"]["kDotP"],
                config["added_mass"]["mDotQ"],
                config["added_mass"]["nDotR"],
            )
        except KeyError:
            added_mass = (0, 0, 0, 0, 0, 0)

        try:
            current = (
                config["default_current"]["x"],
                config["default_current"]["y"],
                config["default_current"]["z"],
            )
        except KeyError:
            current = (0, 0, 0)

        return ModelParams(
            config["model_name"],
            mass,
            collision,
            (
                config["center_of_mass"]["x"],
                config["center_of_mass"]["y"],
                config["center_of_mass"]["z"],
            ),
            (
                config["center_of_volume"]["x"],
                config["center_of_volume"]["y"],
                config["center_of_volume"]["z"],
            ),
            inertia,
            linear_drag,
            quadratic_drag,
            added_mass,
            current,
            [
                (thruster["x"], thruster["y"], thruster["z"])
                for thruster in config["thrusters"]
            ],
            config["control_method"],
        )


def generate_model(input_path: str, output_path: str, config_path: str) -> None:
    # Get the model parameters from the config file and merge them with the global
    # constants
    params = vars(get_model_params_from_config(config_path)) | globals()

    s = open(input_path, "r").read()
    pattern = re.compile(r"@(\w+)")

    # params['foo'] will return the value of foo
    s = re.sub(
        pattern,
        lambda m: str(
            round(params[m.group(1)], 3)
            if isinstance(params[m.group(1)], float)
            else params[m.group(1)]
        ),
        s,
    )
    open(output_path, "w").write(s)


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument(
        "infile",
        type=str,
        help="The full path to the SDF file to inject the configurations into.",
    )
    parser.add_argument(
        "outfile", type=str, help="The full path to the output SDF file."
    )
    parser.add_argument(
        "config", type=str, help="The full path to the YAML configuration file to load."
    )

    args = parser.parse_args()

    generate_model(args.infile, args.outfile, args.config)
