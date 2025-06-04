import heapq
import random
import time
from threading import Thread
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# Classes
class Robotino:
    def __init__(self, robot_id, version, initial_status):
        self.robot_id = robot_id
        self.version = version
        self.status = initial_status
        self.battery_level = 100  # Start with a full battery

    def __str__(self):
        return f"Robotino-{self.robot_id} (Version {self.version}, {self.status}, Battery: {self.battery_level}%)"

    def __lt__(self, other):
        return self.battery_level < other.battery_level

    def drain_battery(self, amount):
        self.battery_level = max(0, self.battery_level - amount)

    def recharge_battery(self):
        """Increase the battery level by 20%, up to a maximum of 100%."""
        if self.battery_level < 100:
            self.battery_level = min(100, self.battery_level + 16)

    def set_status(self, new_status):
        self.status = new_status

class Charger:
    def __init__(self, charger_id, compatible_version):
        self.charger_id = charger_id
        self.compatible_version = compatible_version
        self.current_robotino = None

    def __str__(self):
        status = "Available" if self.current_robotino is None else f"Charging {self.current_robotino}"
        return f"Charger-{self.charger_id} (Compatible with Version {self.compatible_version}, {status})"

    def connect(self, robotino):
        if self.current_robotino is None and robotino.version == self.compatible_version:
            self.current_robotino = robotino
            robotino.set_status("charging")
            return True
        return False

    def disconnect(self):
        if self.current_robotino:
            self.current_robotino = None

# System Initialization
operational_queue = []
charging_queue = []
chargers = [Charger(i + 1, compatible_version=4 if i == 0 else 3) for i in range(6)]

robotinos = [Robotino(robot_id=i + 1, version=4 if i == 0 else 3,
                      initial_status="operational" if i < 3 else "charging")
             for i in range(6)]

for robotino in robotinos[:3]:
    heapq.heappush(operational_queue, robotino)
for robotino in robotinos[3:]:
    heapq.heappush(charging_queue, robotino)

tasks = {i: f"Task-{i}" for i in range(1, 11)}
robotino_tasks = {robotino.robot_id: None for robotino in robotinos}

# Core Functions
def assign_task(robotino):
    for task_id, task in tasks.items():
        if task:
            robotino_tasks[robotino.robot_id] = task
            tasks[task_id] = None
            return

def unassign_task(robotino):
    task = robotino_tasks[robotino.robot_id]
    if task:
        for task_id, task_name in tasks.items():
            if task_name is None:
                tasks[task_id] = task
                break
        robotino_tasks[robotino.robot_id] = None

def find_available_charger(robotino):
    for charger in chargers:
        if charger.compatible_version == robotino.version and charger.current_robotino is None:
            return charger
    return None

def swap_robotinos():
    """Simulates Robotino operation, battery drainage, and task swapping."""
    drained_robotinos = []
    for robotino in operational_queue:
        robotino.drain_battery(random.randint(10, 12))  # Drain battery by a random amount
        if robotino.battery_level < 10:  # Needs charging
            drained_robotinos.append(robotino)

    for low_battery_robotino in drained_robotinos:
        unassign_task(low_battery_robotino)  # Unassign task before charging
        operational_queue.remove(low_battery_robotino)
        heapq.heapify(operational_queue)

        charger = find_available_charger(low_battery_robotino)
        if charger:
            charger.connect(low_battery_robotino)
            heapq.heappush(charging_queue, low_battery_robotino)
        else:
            heapq.heappush(operational_queue, low_battery_robotino)  # Stay operational if no charger

    while len(operational_queue) < 3 and charging_queue:
        ready_robotino = heapq.nlargest(1, charging_queue)[0]
        charging_queue.remove(ready_robotino)
        heapq.heapify(charging_queue)

        for charger in chargers:
            if charger.current_robotino == ready_robotino:
                charger.disconnect()
                break

        ready_robotino.set_status("operational")
        ready_robotino.drain_battery(5)  # Small initial drain
        heapq.heappush(operational_queue, ready_robotino)
        assign_task(ready_robotino)

# Text Output Functions
def display_battery_levels(robotinos):
    print("\nBattery Levels:")
    for robotino in robotinos:
        print(f"  {robotino}")

def display_charger_status(chargers):
    print("\nCharger Status:")
    for charger in chargers:
        print(f"  {charger}")

def display_queue_states(operational_queue, charging_queue):
    print("\nQueue States:")
    print(f"  Operational Queue: {[r.robot_id for r in operational_queue]}")
    print(f"  Charging Queue: {[r.robot_id for r in charging_queue]}")

def display_tasks(robotino_tasks):
    print("\nTask Assignments:")
    for robot_id, task in robotino_tasks.items():
        task_display = task if task else "None"
        print(f"  Robotino-{robot_id}: {task_display}")

# Simulation Logic
def run_simulation():
    for cycle in range(100):  # Simulate 30 cycles
        print(f"\nCycle {cycle + 1}:")
        print("=" * 100)
        swap_robotinos()
        for robotino in charging_queue:
            robotino.recharge_battery()

        # Display text outputs
        display_battery_levels(robotinos)
        display_charger_status(chargers)
        display_queue_states(operational_queue, charging_queue)
        display_tasks(robotino_tasks)
        time.sleep(2)  # Wait for 2 seconds before next cycle

# Run the simulation in a separate thread
simulation_thread = Thread(target=run_simulation, daemon=True)
simulation_thread.start()

# Run the Dash Server
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dcc.Interval(id="interval-component", interval=5 * 1000, n_intervals=0),
    dbc.Row(html.H1("Robotino Simulation Dashboard", className="text-center mb-4")),
    dbc.Row([
        dbc.Col(dcc.Graph(id="battery-levels"), width=6),
        dbc.Col(html.Div(id="task-assignments"), width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id="queue-states"), width=6),
        dbc.Col(dcc.Graph(id="charger-status"), width=6)
    ])
])

@app.callback(
    Output("battery-levels", "figure"),
    Output("task-assignments", "children"),
    Output("queue-states", "figure"),
    Output("charger-status", "figure"),
    Input("interval-component", "n_intervals")
)
def update_dashboard(n_intervals):
    battery_levels = [r.battery_level for r in robotinos]
    robot_ids = [f"R-{r.robot_id}" for r in robotinos]
    battery_fig = go.Figure(go.Bar(x=robot_ids, y=battery_levels, marker_color="blue"))
    task_display = html.Table(children=[
        html.Tr([html.Th("Robot"), html.Th("Task")]),
        *[html.Tr([html.Td(robot_ids[i]), html.Td(robotino_tasks.get(robotinos[i].robot_id, "None"))])
          for i in range(len(robotinos))]
    ], className="table table-hover")
    queue_fig = go.Figure(go.Bar(
        x=["Operational Queue", "Charging Queue"],
        y=[len(operational_queue), len(charging_queue)],
        marker_color=["green", "purple"]
    ))
    charger_status = [c.current_robotino.robot_id if c.current_robotino else "Empty" for c in chargers]
    charger_ids = [f"C-{c.charger_id}" for c in chargers]
    charger_fig = go.Figure(go.Bar(x=charger_ids, y=[1 if s != "Empty" else 0 for s in charger_status], marker_color="cyan"))
    return battery_fig, task_display, queue_fig, charger_fig

if __name__ == "__main__":
    print("Starting simulation. Visit the dashboard at http://127.0.0.1:8080/")
    app.run_server(debug=True, port=8080)
