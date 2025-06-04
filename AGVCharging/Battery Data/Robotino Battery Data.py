import requests
import json


# Function to fetch power management data
def fetch_power_management_data(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()  # Return parsed JSON data
        else:
            print(f"Failed to fetch data from {url}. HTTP Status Code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while connecting to {url}: {e}")
        return None


# Function to calculate battery percentage based on chassis type
def calculate_battery_percentage(voltage, chassis_type):
    if chassis_type == "model3":
        max_voltage = 24.5
        min_voltage = 18.5
    else:  # Assume "model4" for all other cases
        max_voltage = 20.6
        min_voltage = 15.8

    if voltage < min_voltage:
        return 0  # Below minimum voltage
    elif voltage > max_voltage:
        return 100  # Above maximum voltage
    else:
        voltage_range = max_voltage - min_voltage
        return round(((voltage - min_voltage) / voltage_range) * 100)


# Main program
def main():
    # List of Robotino IPs with their chassis types
    robotinos = [
        {"ip": "172.21.20.90", "chassis_type": "model3"},
        {"ip": "172.21.21.90", "chassis_type": "model4"},
        {"ip": "172.21.22.90", "chassis_type": "model3"},
        {"ip": "172.21.23.90", "chassis_type": "model4"},
        {"ip": "172.21.24.90", "chassis_type": "model3"},
        {"ip": "172.21.25.90", "chassis_type": "model4"}
    ]

    # Loop through each Robotino and fetch its data
    for robot in robotinos:
        url = f"http://{robot['ip']}/data/powermanagement"
        print(f"Fetching data from Robotino with IP: {robot['ip']} ({robot['chassis_type']})")

        data = fetch_power_management_data(url)

        if data:
            # Extract voltage and calculate percentage
            voltage = data.get("voltage", None)
            if voltage is not None:
                percentage = calculate_battery_percentage(voltage, robot["chassis_type"])
                print(f"Voltage: {voltage:.2f}V -> Battery: {percentage}%")
            else:
                print("Voltage data not available.")

            # Print the full data for reference
            print(json.dumps(data, indent=4))
        else:
            print(f"No data available for Robotino with IP: {robot['ip']}")
        print("-" * 50)  # Separator for readability


if __name__ == "__main__":
    main()



