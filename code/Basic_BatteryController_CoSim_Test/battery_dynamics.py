import helics as h
import time

# Initialize the HELICS federate
fed = h.helicsCreateValueFederateFromConfig("battery_dynamics_config.json")

# Register the state of charge (SOC) as a publication
soc_pub = h.helicsFederateGetPublication(fed, "battery/SOC")

# Subscribe to control decisions
control_sub = h.helicsFederateGetSubscription(fed, "control/decision")

# Initial SOC
state_of_charge = 0.5  # 50%

# Co-simulation loop
for timestep in range(100):
    h.helicsFederateRequestTime(fed, timestep)

    # Publish the current state of charge
    h.helicsPublicationPublishDouble(soc_pub, state_of_charge)
    
    # Get the control signal from the control script
    control_signal = h.helicsInputGetDouble(control_sub)
    
    # Simulate battery dynamics (charge/discharge)
    if control_signal > 0:
        state_of_charge += 0.01  # Charging
    else:
        state_of_charge -= 0.01  # Discharging
    
    # Ensure SOC is within bounds [0, 1]
    state_of_charge = max(0, min(1, state_of_charge))
    
    print(f"Time: {timestep}, SOC: {state_of_charge}, Control: {control_signal}")
    
    time.sleep(0.1)

# Finalize HELICS federate
h.helicsFederateFinalize(fed)
h.helicsCloseLibrary()
