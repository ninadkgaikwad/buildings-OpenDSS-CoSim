import helics as h
import time
import matplotlib.pyplot as plt

# Initialize the HELICS federate
fed = h.helicsCreateValueFederateFromConfig("battery_visualization_config.json")

# Subscribe to SOC from the dynamics federate
soc_sub = h.helicsFederateGetSubscription(fed, "battery/SOC")

# Subscribe to control decisions from the control federate
control_sub = h.helicsFederateGetSubscription(fed, "control/decision")

# Lists to store data for plotting
time_steps = []
soc_values = []
control_values = []

# Co-simulation loop
for timestep in range(100):
    h.helicsFederateRequestTime(fed, timestep)

    # Get the current SOC and control signal
    soc = h.helicsInputGetDouble(soc_sub)
    control_signal = h.helicsInputGetDouble(control_sub)

    # Store values for plotting
    time_steps.append(timestep)
    soc_values.append(soc)
    control_values.append(control_signal)

    print(f"Time: {timestep}, SOC: {soc}, Control: {control_signal}")

    time.sleep(0.1)

# Plot the data
plt.figure(figsize=(10, 5))
plt.plot(time_steps, soc_values, label='State of Charge (SOC)', color='blue')
plt.plot(time_steps, control_values, label='Control Signal', color='red')
plt.xlabel('Time Step')
plt.ylabel('Value')
plt.title('Battery SOC and Control Signal Over Time')
plt.legend()
plt.grid(True)

# Save the plot as a PNG file
plt.savefig('battery_visualization.png')

# Finalize HELICS federate
h.helicsFederateFinalize(fed)
h.helicsCloseLibrary()
