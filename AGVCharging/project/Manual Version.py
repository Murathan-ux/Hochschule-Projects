import socket
import threading
import time
import math
import logging

HOST = '0.0.0.0' # Host to listen on
PORT = 13000 # Port for server to listen on

JobId = 40 # Start with JobId 1 for Robotino Fleet
MAX_BUFFER_SIZE = 4096 # Maximum buffer size for incoming messages
CURRENT_ROBOTINO_STATE = None

# Configure the logger
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] [%(threadName)s] %(message)s",
    handlers=[
        logging.FileHandler("charging_selection.log"), # Logs to a file
        logging.StreamHandler() # Logs to the console
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
        if distance <= 0.2: # 20 cm threshold
            logging.info(f"charger is in use {charger_id} by Robotino {robot_id}.")
            return True # Charger is occupied
    logging.info(f"charger {charger_id} is not occupied.")
    return False # Charger is not occupied

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
            continue # Skip occupied chargers

        if charger_configurations[charger_id]['type'] != robotino_configurations[robot_id]['type']:
            logging.info(f"skipping charger {charger_id}. Cause: "
                         f"charger model{charger_configurations[charger_id]['type']} does not match "
                         f"robotino model{robotino_configurations[robot_id]['type']}.")
            continue # skip wrong type

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
        return ""

    closest_charger = find_closest_free_charger(robot_id)

    if closest_charger is None:
        print("No available chargers.")
        return ""

    JobId += 1
    command = (
        f"PushJob GotoPosition {JobId} 1 {robot_id} {closest_charger}\n"
    )
    print(f"Sending robot {robot_id} to closest charger (ID: {closest_charger}): {command}")
    return command

def send_all_robots_to_closest_chargers():
    """
    Sends all Robotinos in the fleet to their closest unoccupied chargers.
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
                elif key in {"x", "y", "phi", "batteryvoltage", "current"}:
                    robot_info[key] = float(value)
                elif key in {"charging", "laserwarning", "lasersafety", "emergency", "boxpresent"}:
                    robot_info[key] = bool(int(value))
                elif key == "state":
                    robot_info[key] = value
                elif key == "ipaddress":
                    robot_info[key] = value

            if robot_id is not None:
                fleet_state[robot_id] = robot_info

        print("Updated fleet state:", fleet_state)
    except Exception as e:
        print(f"Error processing fleet state data: {e}")

def handle_incoming_messages(conn, addr):
    """
    Handles incoming messages from the client.
    """
    print('Connected to', addr)

    while True:
        try:
            data = conn.recv(MAX_BUFFER_SIZE)
            if not data: # Connection closed
                print('Connection closed by', addr)
                break
            decoded_data = data.decode('utf-8').strip()
            print('Received message from', addr, ':', decoded_data)
            # Process the fleet state response
            if "FleetState" in decoded_data:
                process_fleet_state_response(decoded_data)
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

def send_message(conn):
    """
    Allows the server to send custom messages to the client from the console.
    """
    global JobId

    while True:
        try:
            message = input(
                'Enter the Message that should be sent (1 for FleetState, 2 for PushJob, 3 for SendToCharger, 4 for SendAllToChargers, 5 for DockAll): ')
            message_to_send = "\n"

            if message == '1':
                message_to_send = "GetFleetState\n"
            elif message == '2':
                robot_id = int(input("Enter Robot ID: "))
                message_to_send = send_robot_to_closest_charger(robot_id)
            elif message == '3':
                robot_id = int(input("Enter Robot ID: "))
                message_to_send = send_robot_to_dock(robot_id)
            elif message == '4':
                send_all_robots_to_closest_chargers()
                continue
            elif message == '5':
                send_all_robots_to_dock()
                continue

            if message_to_send.strip():
                conn.sendall(message_to_send.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message: {e}")
            break

def main():
    """
    Main function to start the server, accept clients, and create threads for handling messages and sending messages.
    """
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
                threading.Thread(target=send_message, args=(conn,)).start()
            except Exception as e:
                print("Error accepting connection:", e)

if __name__ == '__main__':
    main()
