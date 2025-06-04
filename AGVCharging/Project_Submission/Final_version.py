import socket
import threading
import time
import math
import logging
import heapq

HOST = '0.0.0.0'  # Host to listen on
PORT = 13000  # Port for server to listen on

JobId = 50  # Start with JobId 1 for Robotino Fleet
MAX_BUFFER_SIZE = 4096  # Maximum buffer size for incoming messages
CURRENT_ROBOTINO_STATE = None
BATTERY_MINIMUM_PERCENT = 20

# Configure the logger
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] [%(threadName)s] %(message)s",
    handlers=[
        logging.FileHandler("charging_selection.log"),  # Logs to a file
        logging.StreamHandler()  # Logs to the console
    ]
)
logging.info("initialized logging")

# Charger locations as a dictionary with their coordinates and types
charger_configurations = {
    11: {"X": -15.262, "Y": 0.853, "type": 3},
    12: {"X": -14.215, "Y": 0.830, "type": 3},
    13: {"X": -0.162, "Y": 1.525, "type": 3},
    14: {"X": -8.677, "Y": -0.988, "type": 3},
    17: {"X": -0.504, "Y": -0.949, "type": 4},
    18: {"X": -0.276, "Y": 0.067, "type": 4},
}

robotino_configurations = {
    20: {"type": 3},
    21: {"type": 3},
    22: {"type": 3},
    23: {"type": 3},
    24: {"type": 4},
    25: {"type": 4},
}

# Fleet state dictionary: To store robot battery percentages and other info
fleet_state = {}


# Lists to categorize Robotinos
active_robotinos = []
inactive_robotinos = []
drained_robotinos = []
robots_moving_to_charger = []

# Initialize queues for operational and charging Robotinos
operational_queue = [20, 21, 24]  # Robotino IDs: 2 version 3 and 1 version 4
charging_queue = [22, 23, 25]  # Robotino IDs: 2 version 3 and 1 version 4

# Use heapq to maintain priority queue behavior
heapq.heapify(operational_queue)
heapq.heapify(charging_queue)

# Simulated list of chargers (update with actual charger objects if available)
chargers = []  # Example: chargers = [Charger(11), Charger(12), ...]


def calculate_distance(x1, y1, x2, y2):
    """
    Calculates the Euclidean distance between two points (x1, y1) and (x2, y2).
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def is_charger_occupied(charger_id):
    """
    Determines if a charger is occupied based on the current fleet state.
    A charger is considered occupied if a Robotino is within 20 cm of the charger.
    """
    logging.info(f"checking if charger {charger_id} is occupied")
    if charger_id not in charger_configurations:
        logging.info(f"Charger ID {charger_id} is not valid.")
        return False

    charger_coords = charger_configurations[charger_id]
    charger_x, charger_y = charger_coords["X"], charger_coords["Y"]

    for robot_id, robot_info in fleet_state.items():
        robot_x, robot_y = robot_info['x'], robot_info['y']
        distance = calculate_distance(charger_x, charger_y, robot_x, robot_y)
        if distance <= 0.2:  # 20 cm threshold
            logging.info(f"charger is in use {charger_id} by Robotino {robot_id}.")
            return True  # Charger is occupied
    logging.info(f"charger {charger_id} is not occupied.")
    return False  # Charger is not occupied


def find_closest_free_charger(robot_id):
    """
    Finds the closest unoccupied charger for the given Robotino ID based on its position.
    Uses dynamic occupancy checking based on fleet state.
    """
    if robot_id not in fleet_state:
        logging.error(f"skipping search for charger of Robot {robot_id}. Cause: Robot not found in fleet state.")
        return None

    robot_x = fleet_state[robot_id]['x']
    robot_y = fleet_state[robot_id]['y']
    logging.info(f"searching charger for robot: {robot_id} (coordinates: {robot_x}, {robot_y})")

    closest_charger = None
    shortest_distance = float('inf')

    for charger_id, charger_config in charger_configurations.items():
        if is_charger_occupied(charger_id):
            logging.info(f"skipping charger {charger_id}. Cause: occupied charger.")
            continue  # Skip occupied chargers

        if charger_configurations[charger_id]['type'] != robotino_configurations[robot_id]['type']:
            logging.info(f"skipping charger {charger_id}. Cause: "
                         f"charger model{charger_configurations[charger_id]['type']} does not match "
                         f"robotino model{robotino_configurations[robot_id]['type']}.")
            continue  # skip wrong type

        distance = calculate_distance(robot_x, robot_y, charger_config["X"], charger_config["Y"])
        logging.info(
            f"coords charger: {charger_config['X']}, {charger_config['Y']} ||coords robot: {robot_x}, {robot_y} ")
        if distance < shortest_distance:
            closest_charger = charger_id
            logging.info(f"selected charger {charger_id} with distance {distance} as new candidate")
            shortest_distance = distance

    if closest_charger is None:
        logging.error(f"no charger found for robotino{robot_id}.")
    else:
        logging.info(f"closest charger is {closest_charger}")
    return closest_charger


def send_robot_to_closest_charger(robot_id):
    """
    Generates a command to send the robot to the closest unoccupied charger.
    """
    global JobId

    if robot_id not in fleet_state:
        print(f"Robot ID {robot_id} not found in fleet state.")
        return None

    closest_charger = find_closest_free_charger(robot_id)

    if closest_charger is None:
        print("No available chargers.")
        return None

    JobId += 1
    command = (
        f"PushJob GotoPosition {JobId} 1 {robot_id} {closest_charger}\n"
    )
    print(f"Sending robot {robot_id} to closest charger (ID: {closest_charger}): {command}")
    return command


def send_all_robots_to_closest_chargers():
    """
    Sends all Robotinos in the fleet to their closest unoccupied chargers.
    # TODO ensure that no charger is assignment multiple times
    """
    for robot_id in fleet_state.keys():
        command = send_robot_to_closest_charger(robot_id)
        if command:
            print(command)


def send_robot_to_dock(robot_id):
    """
    Sends a command to dock the robot to the charger.
    """
    global JobId
    JobId += 1
    command = f"PushJob BatteryChargerDocking {JobId} 0 {robot_id} DOCK\n"
    print(f"Sending robot {robot_id} to dock: {command}")
    return command


def send_all_robots_to_dock():
    """
    Sends all Robotinos in the fleet to dock at their chargers.
    """
    for robot_id in fleet_state.keys():
        command = send_robot_to_dock(robot_id)
        if command:
            print(command)


def send_robot_to_position(robot_id, target_x, target_y):
    """
    Sends the robot to a specific position.
    # TODO remove? not in use?
    """
    global JobId
    if robot_id not in fleet_state:
        print(f"Robot ID {robot_id} not found in fleet state.")
        return ""

    JobId += 1
    command = f"PushJob GotoPosition {JobId} 1 {robot_id} {target_x} {target_y}\n"
    print(f"Sending robot {robot_id} to position: {command}")
    return command


def process_fleet_state_response(data):
    """
    Processes the fleet state response to extract detailed robot information.
    """
    global fleet_state

    if "FleetState" not in data:
        return

    try:
        robots_data = data.replace("FleetState ", "").split(" , ")

        for robotino in robots_data:
            attributes = robotino.split()
            robot_info = {}
            robot_id = None

            for attr in attributes:
                key, value = attr.split(":")
                if key == "robotinoid":
                    robot_id = int(value)
                elif key in {"x", "y", "phi", "current"}:
                    robot_info[key] = float(value)
                elif key in {"charging", "laserwarning", "lasersafety", "emergency", "boxpresent"}:
                    robot_info[key] = bool(int(value))
                elif key in {"state", "ipaddress"}:
                    robot_info[key] = value
                elif key == "batteryvoltage":
                    try:
                        robot_info["battery_state"] = convert_voltage_to_percentage(voltage=float(value), 
                                                                                    robotino_id=robot_id)
                    except ValueError as e:
                        logging.error("Robotino ID was unexpectedly not set in process_fleet_state: " + str(e))

            if robot_id is not None:
                fleet_state[robot_id] = robot_info

        print("Updated fleet state:", fleet_state)
    except Exception as e:
        print(f"Error processing fleet state data: {e}")


def convert_voltage_to_percentage(voltage, robotino_id):
    """
    Converts voltage of a Robotino's batteries to percentage.
    TODO currently returns values above 100% if Robotino is charging
    :param voltage: Value in Volts from the fleet-state of the master Robotino
    :param robotino_id: Id of the Robotino that is currently processed
    :return:
    """
    if robotino_id is None:
        raise ValueError("robotino_id is None")

    if robotino_configurations[robotino_id]['type'] == 3:
        # correct voltage min/max for model3
        max_voltage = 24.5
        min_voltage =  19.5 # was 18.5 but increased by one because the Robotino battery died before moving to the charger and docking( During Testing)
    else:
        # correct voltage min/max for model4
        max_voltage = 20.6
        min_voltage = 15.8

    # Calculate battery percentage
    voltage_range = max_voltage - min_voltage
    battery_percentage = int(((voltage - min_voltage) / voltage_range) * 100)
    return battery_percentage


def handle_incoming_messages(conn, addr):
    """
    Handles incoming messages from the client.
    """
    print('Connected to', addr)

    while True:
        try:
            data = conn.recv(MAX_BUFFER_SIZE)
            if not data:  # Connection closed
                print('Connection closed by', addr)
                break
            decoded_data = data.decode('utf-8').strip()
            print('Received message from', addr, ':', decoded_data)
            # Process the fleet state response
            if "FleetState" in decoded_data:
                process_fleet_state_response(decoded_data)
            # TODO include other feedback messages (e.g. when a robotino arrives at a location)
        except Exception as e:
            print(f"Error receiving message from {addr}: {e}")
            break


def send_fleet_state(conn):
    """
    Sends the "GetFleetState" message every 2 seconds to maintain the connection.
    """
    while True:
        try:
            message_to_send = "GetFleetState\n"
            conn.sendall(message_to_send.encode('utf-8'))
            print("Sent: GetFleetState")
            time.sleep(2)
        except Exception as e:
            print(f"Error sending fleet state: {e}")
            break


def charging_management(conn):
    """
    Manages the charging process for Robotinos.
    Ensures only a limited number of Robotinos are charging simultaneously
    and puts Robotinos back to work when charged.
    """
    global JobId
    global robots_moving_to_charger

    while True:
        # Log operational queue state for debugging
        logging.info(f"Operational queue: {operational_queue}")
        logging.info(f"Fleet state: {fleet_state}")

        # Filter Robotinos with low battery in the operational queue
        low_battery_robotinos = [
            robot_id for robot_id in operational_queue
            if robot_id in fleet_state and fleet_state[robot_id]['battery_state'] <= BATTERY_MINIMUM_PERCENT
        ]

        # Log any robot IDs missing in the fleet_state
        for robot_id in operational_queue:
            if robot_id not in fleet_state:
                logging.warning(f"Robotino {robot_id} not found in fleet_state.")

        if not low_battery_robotinos:
            logging.info("No Robotino in the operational queue requires charging.")
            time.sleep(5)  # Wait before checking again
            continue

        logging.info(f"Robotinos needing charge: {low_battery_robotinos}")

        # Ensure only a limited number of chargers are in use (currently not being used buc could be used in future for  avoiding multiple robots go to same charger)
        current_charging_count = len(robots_moving_to_charger)
        available_charger_slots = 3 - current_charging_count

        if available_charger_slots <= 0:
            logging.info("All chargers are currently in use.")
            time.sleep(5)  # Wait before checking again
            continue

        # Limit the number of Robotinos sent for charging
        low_battery_robotinos = low_battery_robotinos[:available_charger_slots]

        # Assign chargers and send Robotinos to charge
        for robot_id in low_battery_robotinos:
            if robot_id in robots_moving_to_charger:
                logging.debug(f"Robotino {robot_id} is already being sent to a charger.")
                continue

            message_to_send = send_robot_to_closest_charger(robot_id)
            if not message_to_send:
                logging.info(f"No chargers available for Robotino {robot_id}.")
                continue

            logging.info(f"Assigning Robotino {robot_id} to charger.")
            try:
                # Send Robotino to the charger
                conn.sendall(message_to_send.encode('utf-8'))
                # Send docking command immediatly (sequencd execution handled by job quege of the robotino itself)
                time.sleep(.2) # time for the server to process the first message - might be uneccessary
                message_to_send = send_robot_to_dock(robot_id)
                conn.sendall(message_to_send.encode('utf-8'))

                # Mark Robotino as moving to charger
                robots_moving_to_charger.append(robot_id)

                # Remove from operational queue and add to charging queue
                operational_queue.remove(robot_id)
                charging_queue.append(robot_id)

            except Exception as e:
                logging.error(f"Error sending message for Robotino {robot_id}: {e}")
                break

        # Check if any Robotinos have completed charging
        charged_robotinos = [
            robot_id for robot_id in charging_queue
            if robot_id in fleet_state and fleet_state[robot_id]['battery_state'] > BATTERY_MINIMUM_PERCENT
        ]

        for robot_id in charged_robotinos:
            logging.info(f"Robotino {robot_id} has completed charging.")
            charging_queue.remove(robot_id)
            operational_queue.append(robot_id)

            # Remove from the moving to charger list
            if robot_id in robots_moving_to_charger:
                robots_moving_to_charger.remove(robot_id)

        time.sleep(5)  # Wait before the next iteration


# Function to monitor and print Robotino statuses
def monitor_robotino_status(active_robotinos, inactive_robotinos, drained_robotinos):
    """
    Function to monitor and print Robotino statuses
    :param active_robotinos: list of robotinos that are doing tasks
    :param inactive_robotinos:list of robotinos that are not doing tasks
    :param drained_robotinos: list of robotinos that the battery has been drained
    """
    while True:
        print("\n=== Robotino Status Update ===")
        print(f"Active Robotinos: {active_robotinos}")
        print(f"Inactive Robotinos: {inactive_robotinos}")
        print(f"Drained Robotinos: {drained_robotinos}")
        print("=============================\n")
        time.sleep(120)


def main():
    """
    Main function to start the server, accept clients, and create threads for handling messages and sending messages.
    """
    # Initialize lists to categorize Robotinos
    active_robotinos = []
    inactive_robotinos = []
    drained_robotinos = []

    # Initialize queues for operational and charging Robotinos
    operational_queue = [20, 21, 24]  # Robotino IDs: 2 version 3 and 1 version 4
    charging_queue = [22, 23, 25]  # Robotino IDs: 2 version 3 and 1 version 4

    print("Initialized Robotino lists and queues:")
    print(f"Active Robotinos: {active_robotinos}")
    print(f"Inactive Robotinos: {inactive_robotinos}")
    print(f"Drained Robotinos: {drained_robotinos}")
    print(f"Operational Queue: {operational_queue}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server running and listening on {HOST}:{PORT}")

        while True:
            try:
                conn, addr = s.accept()
                print(f"Client connected from {addr}")

                # Start threads for handling client interaction
                threading.Thread(target=handle_incoming_messages, args=(conn, addr)).start()
                threading.Thread(target=send_fleet_state, args=(conn,)).start()
                threading.Thread(target=charging_management, args=(conn,)).start()
            except Exception as e:
                print("Error accepting connection:", e)


if __name__ == '__main__':
    main()
    print(f"Charging Queue: {charging_queue}")
