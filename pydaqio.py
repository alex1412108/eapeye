# coding= latin-1

import numpy

from PyDAQmx import *

#from PyDAQmx.DAQmxFunctions import *
#from PyDAQmx.DAQmxConstants import *

class MultiChannelAnalogInput():
    """Class to create a multi-channel analog input
    
    Usage: AI = MultiChannelInput(physicalChannel)
        physicalChannel: a string or a list of strings
    optional parameter: limit: tuple or list of tuples, the AI limit values
                        reset: Boolean
    Methods:
        read(name), return the value of the input name
        readAll(), return a dictionary name:value
    """
    def __init__(self,physicalChannel, limit = None, reset = False):
        if type(physicalChannel) == type(""):
            self.physicalChannel = [physicalChannel]
        else:
            self.physicalChannel  =physicalChannel
        self.numberOfChannel = physicalChannel.__len__()
        if limit is None:
            self.limit = dict([(name, (-10.0,10.0)) for name in self.physicalChannel])
        elif type(limit) == tuple:
            self.limit = dict([(name, limit) for name in self.physicalChannel])
        else:
            self.limit = dict([(name, limit[i]) for  i,name in enumerate(self.physicalChannel)])           
        if reset:
            DAQmxResetDevice(physicalChannel[0].split('/')[0] )
    def configure(self):
        # Create one task handle per Channel
        taskHandles = dict([(name,TaskHandle(0)) for name in self.physicalChannel])
        for name in self.physicalChannel:
            DAQmxCreateTask("",byref(taskHandles[name]))
            DAQmxCreateAIVoltageChan(taskHandles[name],name,"",DAQmx_Val_RSE,
                                     self.limit[name][0],self.limit[name][1],
                                     DAQmx_Val_Volts,None)
        self.taskHandles = taskHandles
    def readAll(self):
        return dict([(name,self.read(name)) for name in self.physicalChannel])
    def read(self,name = None):
        if name is None:
            name = self.physicalChannel[0]
        taskHandle = self.taskHandles[name]                    
        DAQmxStartTask(taskHandle)
        data = numpy.zeros((1,), dtype=numpy.float64)
#        data = AI_data_type()
        read = int32()
        DAQmxReadAnalogF64(taskHandle,1,10.0,DAQmx_Val_GroupByChannel,data,1,byref(read),None)
        DAQmxStopTask(taskHandle)
        return data[0]


if __name__ == '__main__':
    task = Task()
    #CreateAOVoltageChan(physicalChannel, nameToAssignToChannel,minVal,maxVal,units,customScaleName)
    task.CreateAOVoltageChan("/Dev1/ao1","",-10.0,10.0,DAQmx_Val_Volts,None)
    #task.CreateAOVoltageChan("/Dev1/ao0","",-10.0,10.0,DAQmx_Val_Volts,None)

    #load cell, displacement laser, bottompotential, bottomcurrent, voltagebox2, toppotential, topcurrent, voltagebox4
    multipleAI = MultiChannelAnalogInput(["Dev1/ai4","Dev1/ai5","Dev1/ai6","Dev1/ai7","Dev1/ai8","Dev1/ai12","Dev1/ai13","Dev1/ai14"])
    multipleAI.configure()

    eapright = 7
    eapleft = 7
    
    task.StartTask()
    #task.WriteAnalogScalarF64(autoStart,timeout,value,reserved)
    task.WriteAnalogScalarF64(1,10.0,eapright,None)
    task.WriteAnalogScalarF64(1,10.0,eapleft,None)
    print (multipleAI.readAll())
    

    task.StopTask()
    

    # last signal sent should 0 both outputs