if robotino.chassis_type == 'model3':
  # correct volatege min/max for model3
    max_voltage = 24.5
    min_voltage = 18.5
else:
  # correct volatege min/max for model4
    max_voltage = 20.6
    min_voltage = 15.8

# Calculate battery percentage
voltage_range = max_voltage - min_voltage
battery_percentage = int(((robot["batteryvoltage"] - min_voltage) / voltage_range) * 100)
