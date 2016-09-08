#functions in pydaqmx
#information was obtained by opening a python environment and using: help(function_name)

task = Task()
    #CreateAOVoltageChan(physicalChannel, nameToAssignToChannel,minVal,maxVal,units,customScaleName)
    task.CreateAOVoltageChan("/Dev1/ao1","",-10.0,10.0,DAQmx_Val_Volts,None)


	#CreateAOVoltageChan(physicalChannel, nameToAssignToChannel, terminalConfig,minVal,maxVal,units,customScaleName)
    task.CreateAIVoltageChan("Dev1/ai0","",DAQmx_Val_RSE,-10.0,10.0,DAQmx_Val_Volts,None)

    #task.WriteAnalogScalarF64(autoStart,timeout,value,reserved)
    task.WriteAnalogScalarF64(1,10.0,eapright,None)

    #task.ReadAnalogScalarF64(timeout,value,reserved)
    task.ReadAnalogScalarF64(10.0,eapright,None)

#DAQmxReadAnalogF64(taskHandle, numSampsPerChan, timeout, fillMode, readArray, arraySizeInSamps, sampsPerChanRead, reserved)
DAQmxReadAnalogF64(taskHandle,1,10.0,DAQmx_Val_GroupByChannel,data,1,byref(read),None)

#DAQmxWriteAnalogF64(taskHandle, numSampsPerChan, autoStart, timeout, dataLayout, writeArray, sampsPerChanWritten, reserved)
DAQmxWriteAnalogF64()