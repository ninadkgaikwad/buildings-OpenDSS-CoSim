# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 16:52:42 2022

@author: ninad
"""

import os
import helics as h
import datetime as dt
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import matplotlib

# Initializing Dataframe to store Values from Subscriptions
Recorder_Storage_List = []

# Folder and File locations
MainDir = os.path.abspath(os.path.dirname(__file__))

# File Path for Storing Results
Recorder_Results_file = os.path.join(MainDir, 'Recorder_Results.csv')

# Creating File Path
Plot_File_Path = os.path.join(MainDir)

start_time = dt.datetime(2021, 1, 1)
stepsize = dt.timedelta(minutes=1)
duration = dt.timedelta(days=1)

fed = h.helicsCreateCombinationFederateFromConfig(
    os.path.join(os.path.dirname(__file__), "Recorder_Federate.json")
)


# register subscriptions
# global
sub_Sine_Value = h.helicsFederateRegisterSubscription(fed, "Sine_Value", "")
sub_Line_Value = h.helicsFederateRegisterSubscription(fed, "Line_Value", "")

# Federate entering Execution Mode
h.helicsFederateEnterExecutingMode(fed)

# Initializing Counter
Counter=-1

times = pd.date_range(start_time, freq=stepsize, end=start_time + duration)
for step, current_time in enumerate(times):
    
    # Increment Counter
    Counter = Counter + 1  


    # Update time in co-simulation
    present_step = (current_time - start_time).total_seconds()
    present_step += 1  # Ensures other federates update before DSS federate
    h.helicsFederateRequestTime(fed, present_step)

    # get signals from other federate
    isupdated = h.helicsInputIsUpdated(sub_Sine_Value)
    if isupdated == 1:
        Sine_Value = h.helicsInputGetString(sub_Sine_Value)
        Sine_Value = json.loads(Sine_Value)
        # Getting Sine
        Sine = Sine_Value['Sine_Value']
    else:
        Sine_Value = {}
        # Getting Sine
        Sine = 0

    print(f"Current time: {current_time}, step: {step}. Received value: Sine = {Sine_Value}")

    isupdated = h.helicsInputIsUpdated(sub_Line_Value)
    if isupdated == 1:
        Line_Value = h.helicsInputGetString(sub_Line_Value)
        Line_Value = json.loads(Line_Value)
        # Getting Line
        Line = Line_Value['Line_Value']
    else:
        Line_Value = {}
        # Getting Line
        Line = 0

    print(f"Current time: {current_time}, step: {step}. Received value: Line = {Line_Value}")
   
    # Add Values to Dataframe
    Recorder_Storage_List.append({'Sine': Sine, 'Line': Line})
    
# Creating DataFrame
Recorder_Storage_DF = pd.DataFrame(Recorder_Storage_List)
    
# Saving Dataframe as CSV
pd.DataFrame(Recorder_Storage_DF).to_csv(Recorder_Results_file)

# Plot and Save Result
plt.plot(Recorder_Storage_DF)

# Plot Embellishments
plt.title('HELICS Basic Simulation Plot')
plt.xlabel('Time')
plt.ylabel('Value')
plt.legend(Recorder_Storage_DF.columns)
plt.tight_layout()

# Saving Plot
plt.savefig(os.path.join(Plot_File_Path, 'HelicsPython_BasicSim_Plot.png'))

# Showing Figure in Console
# plt.show()

h.helicsFederateFinalize(fed)
h.helicsFederateFree(fed)
h.helicsCloseLibrary()