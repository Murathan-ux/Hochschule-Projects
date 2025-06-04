import tkinter as tk
from tkinter import scrolledtext
import socket
import random
import time
from plyer import notification

# Factory configuration: Robotino, chargers, and stations (locations, types, etc.)
factory_config = {
    "robots": {
        "172.21.20.90": {"chassis_type": "model3", "location": [2, 5], "battery_level": 15},  # Battery under 20%
        "172.21.21.90": {"chassis_type": "model3", "location": [6, 7], "battery_level": 50},
        "172.21.22.90": {"chassis_type": "model3", "location": [1, 8], "battery_level": 100},
        "172.21.23.90": {"chassis_type": "model3", "location": [3, 4], "battery_level": 80},
        "172.21.24.90": {"chassis_type": "model4", "location": [5, 1], "battery_level": 15},  # Battery under 20%
        "172.21.25.90": {"chassis_type": "model4", "location": [4, 6], "battery_level": 0},
    },
    "chargers": {
        "Charger1": {"location": [0, 0], "chassis_type": "model3"},
        "Charger2": {"location": [8, 0], "chassis_type": "model3"},
        "Charger3": {"location": [0, 8], "chassis_type": "model3"},
        "Charger4": {"location": [8, 8], "chassis_type": "model3"},
        "Charger5": {"location": [4, 0], "chassis_type": "model4"},
        "Charger6": {"location": [0, 4], "chassis_type": "model4"},
    },
    "stations": {
        "1": {"type": "CP-F-RASS", "location": [-12.313, 4.249], "approach_location": 1},
        "2": {"type": "CP-F-RASS", "location": [-9.824, 4.267], "approach_location": 2},
        "3": {"type": "CP-F-RASS", "location": [-7.398, 4.286], "approach_location": 3},
    }
}

robotino_port = 13000  # UDP port for Robotino communication

# Calculate the distance between two points (Euclidean distance)
def calculate_distance(coord1, coord2):
    return ((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** 0.5

# Find the nearest charger for the selected Robotino based on location and chassis type
def find_nearest_charger(robot_location, chassis_type):
    nearest = None
    min_distance = float("inf")
    for charger, details in factory_config["chargers"].items():
        if details["chassis_type"] == chassis_type:
            distance = calculate_distance(robot_location, details["location"])
            if distance < min_distance:
                min_distance = distance
                nearest = charger
    return nearest

# Send a command to the selected Robotino (e.g., movement or docking commands)
def send_command(command):
    ip = selected_ip.get()  # Get the selected robot IP from the dropdown
    try:
        message = f"{command}"
        udp_socket.sendto(message.encode(), (ip, robotino_port))  # Send command via UDP
        log_message(f"Sent to {ip}: {command}")  # Log the sent command
        # Simulate acknowledgment from Robotino
        time.sleep(0.5)  # Simulating communication delay
        log_message(f"Robotino {ip} acknowledged: {command}")  # Log acknowledgment
    except Exception as e:
        log_message(f"Error sending to {ip}: {e}")  # Log any error

# Simulate real-time Robotino movement (randomized for demonstration)
def update_robot_location():
    ip = selected_ip.get()  # Get selected Robotino IP
    robot_location = factory_config["robots"][ip]["location"]
    robot_location[0] += random.randint(-1, 1)  # Simulate X-axis movement
    robot_location[1] += random.randint(-1, 1)  # Simulate Y-axis movement
    factory_config["robots"][ip]["location"] = robot_location  # Update location
    display_locations()  # Update locations display
    draw_factory()  # Redraw the factory visualization

# Display Robotino and charger locations in the text area
def display_locations():
    locations_text.delete(1.0, tk.END)  # Clear the text area
    locations_text.insert(tk.END, "Robotino Locations:\n")
    for ip, details in factory_config["robots"].items():
        locations_text.insert(tk.END, f"{ip} (Type: {details['chassis_type']}): {details['location']} - Battery: {details['battery_level']}%\n")
    locations_text.insert(tk.END, "\nCharger Locations:\n")
    for charger, details in factory_config["chargers"].items():
        locations_text.insert(
            tk.END, f"{charger} (Type: {details['chassis_type']}): {details['location']}\n"
        )
    locations_text.insert(tk.END, "\nStations Locations:\n")
    for station_id, details in factory_config["stations"].items():
        locations_text.insert(
            tk.END, f"Station {station_id} (Type: {details['type']}): {details['location']}\n"
        )

# Draw factory grid (visualization of locations for robots, chargers, and stations)
def draw_factory():
    canvas.delete("all")  # Clear the canvas
    # Draw Robotinos
    for ip, details in factory_config["robots"].items():
        x, y = details["location"]
        battery_level = details["battery_level"]
        color = "green" if battery_level >= 70 else "yellow" if battery_level >= 50 else "blue" if battery_level >= 30 else "red"
        canvas.create_oval(
            x * 50 + 10, y * 50 + 10, x * 50 + 40, y * 50 + 40, fill=color
        )  # Draw robot with battery color
        canvas.create_text(x * 50 + 25, y * 50 + 25, text=f"{ip}\n{battery_level}%", fill="black", font=("Arial", 13))

    # Draw Chargers
    for charger, details in factory_config["chargers"].items():
        x, y = details["location"]
        canvas.create_rectangle(
            x * 50 + 15, y * 50 + 15, x * 50 + 35, y * 50 + 35, fill="green"
        )  # Draw charger as green rectangle
        canvas.create_text(
            x * 50 + 25, y * 50 + 25, text=charger, fill="black", font=("Arial", 10)
        )  # Display charger ID

    # Draw Stations
    for station_id, details in factory_config["stations"].items():
        x, y = details["location"]
        canvas.create_rectangle(
            x * 50 + 15, y * 50 + 15, x * 50 + 35, y * 50 + 35, fill="yellow"
        )  # Draw station as yellow rectangle
        canvas.create_text(
            x * 50 + 25, y * 50 + 25, text=f"Station {station_id}", fill="black", font=("Arial", 10)
        )  # Display station ID

# Log messages in the GUI
def log_message(message):
    log_text.insert(tk.END, f"{message}\n")  # Insert log message
    log_text.see(tk.END)  # Scroll to the latest log message

# Function to automatically send Robotino to charge if battery is below 20%
def auto_charge_if_low_battery():
    for ip, robot_details in factory_config["robots"].items():
        battery_level = robot_details["battery_level"]
        if battery_level < 20:
            log_message(f"Battery level of Robot {ip} is {battery_level}%. Sending to charge.")
            robot_location = robot_details["location"]
            chassis_type = robot_details["chassis_type"]
            nearest_charger = find_nearest_charger(robot_location, chassis_type)  # Find nearest charger
            if nearest_charger:
                charger_location = factory_config["chargers"][nearest_charger]["location"]
                move_robot_to_charger(ip, robot_location, charger_location)
                log_message(f"Robot {ip} heading to {nearest_charger} at {charger_location}.")
            else:
                log_message(f"No charger available for Robot {ip}.")
        else:
            log_message(f"Battery level of Robot {ip} is {battery_level}%. No need to charge.")  # Log if no charging needed

# Animate robot movement to the charger
def move_robot_to_charger(ip, start_location, charger_location):
    robot_location = start_location[:]
    x1, y1 = robot_location
    x2, y2 = charger_location
    steps = 20  # Number of steps for smooth animation
    dx = (x2 - x1) / steps
    dy = (y2 - y1) / steps

    def move_step(step):
        nonlocal x1, y1
        if step <= steps:
            x1 += dx
            y1 += dy
            factory_config["robots"][ip]["location"] = [x1, y1]
            draw_factory()  # Redraw the factory with updated position
            app.after(100, move_step, step + 1)
        else:
            log_message(f"Robot {ip} has docked at charger at {charger_location}. Charging...")
            factory_config["robots"][ip]["battery_level"] = 100  # Set battery to 100% when docked

    move_step(1)  # Start the movement

# Notification function to send alerts
def send_notification(title, message, max_notifications=5, duration=10):
    for _ in range(max_notifications):
        notification.notify(
            title=title,
            message=message,
            app_name='AGV Charging',  # Optional: Name of your application
            timeout=duration  # Notification appears for 5 seconds
        )
        time.sleep(duration)  # Sleep for 5 seconds before sending next notification

# GUI setup (using Tkinter for visualization and interaction)
app = tk.Tk()
app.title("IoT Factory: Robotino Control and Visualization")

# Robot selection frame
frame_robot = tk.Frame(app)
frame_robot.pack(pady=5)
tk.Label(frame_robot, text="Select Robotino IP:").pack(side=tk.LEFT, padx=5)
selected_ip = tk.StringVar(value=list(factory_config["robots"].keys())[0])
ip_menu = tk.OptionMenu(frame_robot, selected_ip, *factory_config["robots"].keys())
ip_menu.pack(side=tk.LEFT, padx=5)

# Command buttons frame
frame_commands = tk.Frame(app)
frame_commands.pack(pady=5)

# Define functions for buttons
def command_goto_charger():
    ip = selected_ip.get()  # Get the selected robot IP
    robot_location = factory_config["robots"][ip]["location"]
    chassis_type = factory_config["robots"][ip]["chassis_type"]
    nearest_charger = find_nearest_charger(robot_location, chassis_type)
    if nearest_charger:
        charger_location = factory_config["chargers"][nearest_charger]["location"]
        move_robot_to_charger(ip, robot_location, charger_location)

tk.Button(frame_commands, text="Send to Nearest Charger", command=command_goto_charger, bg="orange").pack(side=tk.LEFT, padx=5)
tk.Button(frame_commands, text="Auto Charge If Battery < 20%", command=auto_charge_if_low_battery, bg="red").pack(side=tk.LEFT, padx=5)
tk.Button(frame_commands, text="Send Low Battery Notification", command=lambda: send_notification("Low Battery Alert", "Robotino 20, 24, and 25 battery level is below the threshold. Please recharge."), bg="blue").pack(side=tk.LEFT, padx=5)

# Visualization canvas for displaying factory layout
canvas = tk.Canvas(app, width=500, height=500, bg="lightgrey")
canvas.pack(pady=10)

# Log display area (for monitoring commands and actions)
log_text = scrolledtext.ScrolledText(app, width=70, height=10)
log_text.pack(pady=5)

# Locations display area (for robot and charger positions)
locations_text = scrolledtext.ScrolledText(app, width=70, height=10)
locations_text.pack(pady=5)

# UDP socket setup for communication with Robotinos
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Initial display of locations and factory grid
display_locations()
draw_factory()

# Start the GUI loop
app.mainloop()

