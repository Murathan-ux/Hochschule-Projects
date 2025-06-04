import socket
import threading
import time
import math

HOST = '0.0.0.0'  # Host to listen on
PORT = 13000  # Port for server to listen on

JobId = 10  # Start with JobId 1 for Robotino Fleet
MAX_BUFFER_SIZE = 4096  # Maximum buffer size for incoming messages
CURRENT_ROBOTINO_STATE = None

# Charger locations as a dictionary with their coordinates and types
charger_locations = {
    11: {"X": -15.0, "Y": 853.0, "type": "model3"},
    12: {"X": -14.0, "Y": 830.0, "type": "model3"},
    13: {"X": -162.0, "Y": 1.51, "type": "model3"},
    14: {"X": -8667.0, "Y": -988.0, "type": "model3"},
    17: {"X": -504.0, "Y": -949.0, "type": "model4"},
    18: {"X": -276.0, "Y": 67.0, "type": "model4"},
}

# Keep track of occupied chargers
occupied_chargers = set()  # Set of charger IDs currently in use

# Fleet state dictionary: To store robot battery percentages and other info
fleet_state = {}

def calculate_distance(x1, y1, x2, y2):
    """
    Calculates the Euclidean distance between two points (x1, y1) and (x2, y2).
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def find_closest_free_charger(robot_id):
    """
    Finds the closest unoccupied charger for the given robot ID based on its position.
    """
    if robot_id not in fleet_state:
        print(f"Robot ID {robot_id} not found in fleet state.")
        return None

    robot_x = fleet_state[robot_id]['x']
    robot_y = fleet_state[robot_id]['y']

    closest_charger = None
    shortest_distance = float('inf')

    for charger_id, location in charger_locations.items():
        if charger_id in occupied_chargers:
            continue  # Skip occupied chargers

        distance = calculate_distance(robot_x, robot_y, location["X"], location["Y"])
        if distance < shortest_distance:
            closest_charger = charger_id
            shortest_distance = distance

    return closest_charger

def send_robot_to_closest_charger(robot_id):
    """
    Generates a command to send the robot to the closest unoccupied charger.
    """
    global JobId

    if robot_id not in fleet_state:
        print(f"Robot ID {robot_id} not found in fleet state.")
        return ""

    robot_x = fleet_state[robot_id]['x']
    robot_y = fleet_state[robot_id]['y']

    # Find the closest free charger
    closest_charger = find_closest_free_charger(robot_id)

    if closest_charger is None:
        print("No available chargers.")
        return ""

    # Mark the charger as occupied
    occupied_chargers.add(closest_charger)

    # Create the command to go to the charger
    charger_coords = charger_locations[closest_charger]
    JobId += 1
    command = (
        f"PushJob GotoPosition {JobId} 1 21 {closest_charger}\n"
    )
    print(f"Sending robot {robot_id} to closest charger (ID: {closest_charger}): {command}")
    return command

def send_robot_to_dock(robot_id):
    """
    Sends a command to dock the robot to the charger.
    """
    global JobId
    JobId += 1
    command = f"PushJob BatteryChargerDocking {JobId} 0 {robot_id} DOCK\n"
    print(f"Sending robot {robot_id} to dock: {command}")
    return command

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

def release_charger(charger_id):
    """
    Releases a charger, making it available again.
    """
    if charger_id in occupied_chargers:
        occupied_chargers.remove(charger_id)
        print(f"Charger {charger_id} is now free.")

def process_fleet_state_response(data):
    """
    Processes the fleet state response to extract detailed robot information.
    """
    global fleet_state

    if "FleetState" not in data:
        # Stopping because data did not include correct Keyword
        return

    try:
        # Parse the detailed robot information from the data
        robots_data = data.replace("FleetState ", "").split(" , ")

        for robotino in robots_data:
            # Retrieve key-value pairs for each robotino
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
            if not data:  # Connection closed
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
                'Enter the Message that should be sent (1 for FleetState, 2 for PushJob, 3 for SendToCharger): ')
            message_to_send = "\n"

            if message == '1':
                message_to_send = "GetFleetState\n"
            elif message == '2':
                # Job 2: Send to closest charger
                robot_id = 21  # Replace with actual robot ID
                message_to_send = send_robot_to_closest_charger(robot_id)
            elif message == '3':
                # Job 3: Dock to charger (Assume robot 21 needs to dock)
                message_to_send = send_robot_to_dock(21)
            elif message == '4':
                # Job 4: Go to specific position (e.g., X=10, Y=20)
                message_to_send = send_robot_to_position(21, 10, 20)

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
