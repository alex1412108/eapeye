""" Simple example of analog output
    This example outputs 'value' on ao0
"""

#from PyDAQmx import Task
from PyDAQmx import *
import numpy as np

value = 0

task = Task()
task.CreateAOVoltageChan("/Dev1/ao1","",-10.0,10.0,DAQmx_Val_Volts,None)
task.StartTask()
task.WriteAnalogScalarF64(1,10.0,value,None)
task.StopTask()
