# Management of Charging Stations for a Fleet of Logistics Robots. Simulation of a Robotic Sorting Center.

## Main Assumptions

Packages continuously arrive at the receiving points of the sorting logistics center, which robots must sort and deliver to the corresponding destination points within the center.

The sorting center is a rectangular area divided into cells, some of which are marked as:
- Receiving points for packages,
- Destination points for packages,
- Charging stations for robots.

Robots can move forward and turn in one of four directions. Robots perform actions based on commands from the control system, with each action taking a discrete amount of time specified by the model:
- **Idle** (time determined by the control system),
- **Move forward** one cell,
- **Turn 90 degrees**,
- **Pick up a package** (at a receiving point),
- **Deliver a package** (at a destination point),
- **Charge** (at a charging station).

When a robot picks up a package, its destination is randomly selected.

All robots in the warehouse have a minimum charge threshold. If a robot is without a package and its charge level is less than or equal to the threshold, it goes to the charging station that is expected to be available first.

A collision between robots is defined as the simultaneous use of the same cell by two robots:
- Both are in the same cell,
- Both are moving into the same cell,
- One is moving into a cell occupied by the other,
- One is moving into a cell from which the other is moving.

## Installation
1. It is assumed that the following are already installed:
    - Python 3.12,
    - [SimPy](https://github.com/esemble/simpy) (a Python library).

## Model Configuration

The configuration is defined by several `.json` files and a selected algorithm. The simulation is launched from the command line.

### Warehouse Map
The warehouse configuration is specified in a `.json` file containing:
- `span` - the distance between cells,
- `cells` - a rectangular 2D array of cells (1st coordinate - row from top to bottom, 2nd coordinate - column from left to right), each of which may contain the following optional fields:
    - `free` - whether a robot can be in the cell (default: `true`),
    - `inputId` - unique ID of the receiving point (default: none),
    - `outputId` - unique ID of the destination point (default: none),
    - `chargeId` - unique ID of the charging station (default: none).

### Robot Properties
A robot is created with the following parameters:
- `timeToMove` - time to move forward one cell,
- `timeToTurn` - time to turn 90 degrees,
- `timeToTake` - time to pick up a package,
- `timeToPut` - time to deliver a package,
- `timeToCharge` - time to charge to 100%,
- `charge_to_turn` - charge consumed to turn,
- `charge_to_go` - charge consumed to move forward one cell,
- `charge_to_take` - charge consumed to pick up a package,
- `charge_to_put` - charge consumed to deliver a package,
- `charge_to_stop` - charge consumed to stop,
- `charge_to_start` - charge consumed to start moving.

### Robot Placement
The model also specifies the initial placement of robots in the warehouse. The parameters include:
- `robots` - a list where each element contains:
    - `id` - optional ID,
    - `x` - position along the 1st coordinate (starting from 0),
    - `y` - position along the 2nd coordinate (starting from 0),
    - `direction` - one of the following directions:
        - `up` - upwards,
        - `left` - to the left,
        - `down` - downwards,
        - `right` - to the right.

## Simulation Architecture

The model is divided into two parts: the control system and the (controlled) warehouse model.

Before the simulation starts, the warehouse model:
1. Reads the configuration files,
2. Places the robots and notifies the control system about each one,
3. Requests the first action for each robot from the control system.

During execution, the model repeats the following steps:
1. Checks if the robot's action can be executed.
2. If possible, executes the robot's action.
3. If the action cannot be executed, an error occurs or the control system is notified, depending on the type of error.
4. Once the action is completed, requests the next action from the control system.

When the simulation ends (either after a specified time or after delivering a specified number of packages), the warehouse model outputs the required results.

### Controlled Warehouse Model

#### Warehouse Model Structure
- [/brains/](/brains/) - control algorithms,
- [/mail_factories/](/mail_factories/) - package generators,
- [/maps/](/maps/) - maps, including the main map and additional ones storing extra information,
- [/structures.py](/structures.py) - immutable data structures,
- [/modelling.py](/modelling.py) - the main `Model` class, which ties together the other classes and takes control after receiving the simulation command,
- [/brains/brain.py](/brains/brain.py) - the abstract `Brain` class, defining the control system interface,
- [/cell.py](/cell.py) - the `Cell` class, implementing a map cell,
- [/robot.py](/robot.py) - the `Robot` class, performing actions.

#### Before Execution
1. For each robot, the model reserves the cell corresponding to its initial position.
2. For each robot, the model calls `Brain.add_robot`.
3. For each robot, the model requests the first action by calling `Brain.get_next_action`.

#### During Execution
After receiving the next action for a robot, the model executes it as follows:
- **Idle**: The model adds an event indicating that the robot will finish the action after the specified time.
- **Move**: The model reserves the next cell, adds an event for the movement time, and cancels the reservation of the previous cell.
- **Charge**: The robot charges.
- **Pick up**: The robot picks up a package.
- **Deliver**: The robot delivers a package.

After processing the action, the model requests the next action for the robot by calling `Brain.get_next_action`.

### Control System Model

#### Interface
The control system model must be implemented in Python as a class inheriting from the `Brain` class, with the following methods:
- `add_robot(Robot)`, called by the warehouse model for each added robot before the simulation starts.
- `get_next_action(Robot) -> Robot.Action`, called by the warehouse model for each robot, returning the next action for the robot.

#### Information About Warehouse State
The control system can access all information about the current state of the warehouse model through the `_model` field (an instance of the `Model` class) contained in the `Brain` class.

The `Model` class contains:
- The immutable part - the warehouse map (`map` field),
- The mutable part - the state of the robots (`robots` field).

The warehouse map can be accessed through the `Map` fields:
- `inputs` - list of receiving point coordinates,
- `outputs` - list of destination point coordinates,
- `chargers` - list of charging station coordinates,
- `inputs_ids` - list of receiving point IDs,
- `outputs_ids` - list of destination point IDs,
- `charge_ids` - list of charging station IDs.

Each cell contains the following immutable fields:
- `free` - whether a robot can be in the cell,
- `input_id` - receiving point ID or `None` if absent,
- `output_id` - destination point ID or `None` if absent,
- `charge_id` - charging station ID or `None` if absent,
- `reserved` - whether the cell is reserved by a robot (other robots cannot move into it).

Each robot contains the following immutable fields, corresponding to the configuration:
- `id` - robot ID (if specified in the configuration, otherwise `None`),
- `type` - robot type, containing information about the robot's properties.

Since the mutable part of the model consists only of the robots' state, the current state of the warehouse model can be determined from the `Robot` class fields:
- `position.x`, `position.y` - integer coordinates of the cell where the robot is located (starting from 0),
- `direction` - one of four directions,
- `battery_capacity` - maximum battery capacity,
- `current_charge` - current charge level,
- `robot_is_standing_` (`bool`) - indicates whether the robot is stationary or moving,
- `is_going_to_charger_` (`bool`) - indicates whether the robot is heading to a charging station,
- `mail` - the package the robot is carrying or `None` if no package is being carried:
    - `mail.id` (`int`) - unique package ID,
    - `mail.destination` (`int`) - destination point ID.
