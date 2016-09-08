d = daq.getDevices

s = daq.createSession('ni')

ch_o = addAnalogOutputChannel(s,'Dev1',0:1,'Voltage')
% ch_i = addAnalogInputChannel(s,'Dev2', 0:1, 'Voltage');
% ch_i(1).TerminalConfig = 'SingleEnded';
 ch_i = addAnalogInputChannel(s,'Dev1',0:8,'Voltage')
 ch_i(1).TerminalConfig = 'SingleEnded';
%addAnalogInputChannel(s,'Dev2',1,'Voltage')
 
% ch = addAnalogInputChannel(s,'Dev2',16,'Voltage' )
% ch.TerminalConfig = 'SingleEnded';

%ch(2).Range = [-10.0 10.0];
% addAnalogOutputChannel(s,'Dev2',0,'Voltage')
% addAnalogInputChannel(s,'Dev2',0,'Voltage')
% addAnalogInputChannel(s,'Dev2',1,'Voltage')
 
% ch = addAnalogInputChannel(s,'Dev2',2,'Voltage' )
% ch.TerminalConfig = 'SingleEnded';


% define variables
sample_rate = 100;      % variable 50 samples per second
f = 0.5;                % variable frequency 1Hz

s.Rate = sample_rate;          % take 60 samples per second

%duration = 20;                 % for 20 secs



output = 1 + square(0:f*2*pi/sample_rate:20*pi)';        % start     :     frequency * (step size) / sample rate     :     desired length of time (s) * frequency * step size (per second)

switch_lo = 0*square(0:f*2*pi/sample_rate:20*pi)';      % matrix of 0, same length as output signal
switch_hi = 1+0*square(0:f*2*pi/sample_rate:20*pi)';    % matrix of 1, same length as  output signal

%queueOutputData(s,output);
%queueOutputData(s,  [switch_lo,switch_lo; switch_hi, output; switch_lo, switch_lo]);     % Use the queueOutputData function to generate multiple scans. Data should be a M-by-N matrix where M is the number of scans you want and N is the number of channels in the session
queueOutputData(s,  [switch_hi, output]); 
plot(output);

[data, timestamps, triggerTime] = s.startForeground;
plot(timestamps, data);
xlabel('Time (seconds)'); ylabel('Voltage (Volts)');
title(['Clocked Data Triggered on: ' datestr(triggerTime)])


filename = sprintf('file_%s.csv', datestr(now, 30));
%FL = fopen(filename,'w');

csvwrite(filename,data)




%% ANOTHER WAY TO DO IT: 
% output_data = 10*sin(linspace(0,2*pi,1000)');
% queueOutputData(s,output_data)
% % output_data = 10*sin(linspace(2*pi,3*pi,1000)');
% % queueOutputData(s,output_data)
% plot(output_data);
% title('Output Data Queued');
% [captured_data,time] = s.startForeground();
% %plot(time,captured_data);
% ylabel('Voltage');
% xlabel('Time');
% title('Acquired Signal');





