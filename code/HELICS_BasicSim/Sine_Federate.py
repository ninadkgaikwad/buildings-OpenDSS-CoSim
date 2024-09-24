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
A = 2
F = 10
P = 0
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
    os.path.join(os.path.dirname(__file__), "Sine_Federate.json")
)

# register publications
# global
pub_Sine_Value = h.helicsFederateRegisterGlobalTypePublication(fed, "Sine_Value", "String", "")

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
    h.helicsFederateRequestTime(fed, present_step)

    # Compute Sine
    Sine = A*np.sin(2*np.pi*F*time+np.radians(P))

    Sine_Value = {'Sine_Value': float(Sine)}
    print(Sine_Value)


    # publish to other federates

    h.helicsPublicationPublishString(pub_Sine_Value, json.dumps(Sine_Value))
    print(f"Current time: {current_time}, step: {step}. Sent value: Sine_Value = {Sine_Value}")


    # Incrementing time
    time = time + ts

h.helicsFederateFinalize(fed)
h.helicsFederateFree(fed)
h.helicsCloseLibrary()