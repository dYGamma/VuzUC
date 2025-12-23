clear
clc
%Задание 1
load twotankdata
time = ((0:length(u)-1)*0.2)';
t = time;
yout = y;
u_tst = [time, u];
y_tst = [time, y];

%Задание 2
% bode(amx2221)


%Задание 3
% y_tst = [1,1];
% sim('LR_3_var15')
% time = out.y_prot.Time;
% y=out.y_prot.Data;
% u = out.u_prot.Data;
% u_tst = [time, u];
% y_tst = [time, y];

%Задание 4
% u1 = downsample(u, 100);


%Задание 5
% u = out.ScopeData1.signals(1).values;
% y = out.ScopeData1.signals(2).values;
% time = out.tout;
