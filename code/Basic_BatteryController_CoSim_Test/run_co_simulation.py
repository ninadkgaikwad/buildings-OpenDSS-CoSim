import subprocess
import time

def start_helics_broker():
    """Start the HELICS broker."""
    print("Starting HELICS broker...")
    broker_process = subprocess.Popen(
        ['helics_broker', '--federates=3', '--loglevel=info'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return broker_process

def run_battery_dynamics():
    """Run the battery dynamics script."""
    print("Running battery dynamics...")
    dynamics_process = subprocess.Popen(
        ['python', 'battery_dynamics.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return dynamics_process

def run_battery_control():
    """Run the battery control script."""
    print("Running battery control...")
    control_process = subprocess.Popen(
        ['python', 'battery_control.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return control_process

def run_battery_visualization():
    """Run the battery visualization script."""
    print("Running battery visualization...")
    visualization_process = subprocess.Popen(
        ['python', 'battery_visualization.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return visualization_process

def main():
    # Start the HELICS broker
    broker_process = start_helics_broker()
    
    # Wait for the broker to initialize
    time.sleep(2)
    
    # Start the battery dynamics federate
    dynamics_process = run_battery_dynamics()
    
    # Start the battery control federate
    control_process = run_battery_control()

    # Start the battery visualization federate
    visualization_process = run_battery_visualization()

    # Wait for the processes to complete
    try:
        dynamics_process.communicate()
        control_process.communicate()
        visualization_process.communicate()
    except KeyboardInterrupt:
        print("Terminating simulation...")
    
    # Terminate the broker process
    broker_process.terminate()

if __name__ == "__main__":
    main()
