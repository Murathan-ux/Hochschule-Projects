# Final Version of Robotino Management System

# IoT Factory Robotino System

As shown here, we have an IoT factory with a group of Robotinos, which are robots that assist and perform various tasks in the factory. 

Previously, the factory relied on a simple charging system that was inefficient and ineffective. To address this issue, we implemented a dynamic system based on two collaborative groups of Robotinos. 

### Key Features of the New System:
- **Task Collaboration**: The Robotinos divide tasks dynamically between two groups.
- **Automatic Charging**: Robotinos automatically go to charge when their battery is low.
- **Dynamic Switching**: Fully charged Robotinos switch groups to replace those with drained batteries.
- **Reliable Communication**: The system ensures seamless switching and task allocation using reliable methods and data connections.

This system enhances efficiency and ensures the continuous operation of the factory with minimal downtime.
## Key Features

- **Dynamic Queue Management**: Robotinos are dynamically allocated between the charging and operational queues.
- **Efficient Queue Handling**: The system leverages Python's `heapq` to prioritize and manage the Robotinos.
- **TCP Server Integration**: The system is controlled through a TCP server that communicates with the master Robotino. The server fetches the current state of the fleet using the `Get_fleetstate` command.

## How It Works

1. **Queue Management**: The robotinos are split into two main categories:
    - **Charging Queue**: Robotinos that are charging.
    - **Operational Queue**: Robotinos that are actively performing tasks.

2. **Heap-based Prioritization**: The system uses `heapq` for efficient queue management. This allows for quick decision-making on whether a Robotino should be in a charging state or operational state based on its needs and the fleet's overall state.

3. **Master Robotino Control**: The logic runs through a TCP server that interacts with the master Robotino. The master Robotino regularly queries the fleet's status with the `Get_fleetstate` command, ensuring that the system adapts to the changing environment.

4. **Flawless Operation**: The system has been rigorously tested in real-world conditions, and the queue management and automation processes work without fail.

# Manual Version

The `Manual Version.py` is a version of the system where the user can manually connect to the TCP server and manage the Robotinos by sending commands. It serves as a **command center** for controlling the Robotinos and is designed to provide flexibility for manual operation.

## Key Features

- **Manual Control**: Users can connect to the TCP server and send commands to Robotinos.
- **Command Center**: Functions as a central hub where the status of Robotinos can be monitored and controlled.
- **Reliable and Flawless**: The system has been tested and proven to work flawlessly and reliably in real-world scenarios.

## How It Works

1. **TCP Server Connection**: The user connects to the TCP server via the `group1integration.py` script.
2. **Manual Command Execution**: Once connected, users can send various commands to manage the Robotinos, such as directing them to specific tasks or charging stations.
3. **Command Center**: The system operates as a control center where the user can see the state of each Robotino and perform manual interventions as needed.

## Usage

To use the system, simply run the `group1integration.py` script and connect to the TCP server. Once connected, you can manually send commands to manage the Robotinos by jobs IDs for example: 1,2,3.

# Main_simulation

The `simulation.py` is a dynamic system that simulates Robotino operations, including battery drainage, task assignment, and charging. It utilizes Dash for real-time visualization and displays various metrics such as battery levels, charger statuses, queue states, and task assignments. This simulation includes both a backend system for managing robot states and a frontend dashboard for monitoring the simulation.

## Key Features

- **Robotino Management**: The system models Robotinos with different versions, battery levels, and operational states. Each Robotino can be tasked and recharged.
- **Dynamic Task Assignment**: Tasks are assigned to operational Robotinos and unassigned if their battery is low.
- **Charger Management**: Robotinos need to recharge, and the system automatically finds available chargers based on compatibility.
- **Real-Time Dashboard**: The dashboard displays real-time updates of battery levels, task assignments, queue states, and charger statuses.
- **Simulated Operations**: Robotinos drain their battery during operation, need recharging, and switch between operational and charging queues based on battery status.




