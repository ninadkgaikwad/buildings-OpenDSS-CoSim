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

# Sine Simulation Inputs
A = 3
B = 10
TimeStep = 0.001

# initializing time and ts
time = np.array([0])

ts = np.array([TimeStep])

# Folder and File locations
MainDir = os.path.abspath(os.path.dirname(__file__))

start_time = dt.datetime(2021, 1, 1)
stepsize = dt.timedelta(minutes=1)
duration = dt.timedelta(days=1)

fed = h.helicsCreateCombinationFederateFromConfig(
    os.path.join(os.path.dirname(__file__), "Line_Federate.json")
)

# register publications
# global
pub_Line_Value = h.helicsFederateRegisterGlobalTypePublication(fed, "Line_Value", "String", "")

# register subscriptions
# global
sub_Sine_Value = h.helicsFederateRegisterSubscription(fed, "Sine_Value", "")

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


    
    # Compute Line
    Line = A*time + B + Sine

    Line_Value = {'Line_Value': float(Line)}
    print(Line_Value)


    # publish to other federates

    h.helicsPublicationPublishString(pub_Line_Value, json.dumps(Line_Value))
    print(f"Current time: {current_time}, step: {step}. Sent value: Line_Value = {Line_Value}")


    # Incrementing time
    time = time + ts

h.helicsFederateFinalize(fed)
h.helicsFederateFree(fed)
h.helicsCloseLibrary()