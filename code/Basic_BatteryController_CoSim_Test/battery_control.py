import helics as h
import time

# Initialize the HELICS federate
fed = h.helicsCreateValueFederateFromConfig("battery_control_config.json")

# Subscribe to SOC from the dynamics federate
soc_sub = h.helicsFederateGetSubscription(fed, "battery/SOC")

# Register control decision as a publication
control_pub = h.helicsFederateGetPublication(fed, "control/decision")

# Co-simulation loop
for timestep in range(100):
    h.helicsFederateRequestTime(fed, timestep)
    
    # Get the current state of charge
    soc = h.helicsInputGetDouble(soc_sub)
    
    # Simple control logic: if SOC < 0.5, charge; if SOC >= 0.5, discharge
    if soc < 0.5:
        control_signal = 1  # Charge
    else:
        control_signal = -1  # Discharge
    
    # Publish the control decision
    h.helicsPublicationPublishDouble(control_pub, control_signal)
    
    print(f"Time: {timestep}, SOC: {soc}, Control Signal: {control_signal}")
    
    time.sleep(0.1)

# Finalize HELICS federate
h.helicsFederateFinalize(fed)
h.helicsCloseLibrary()
