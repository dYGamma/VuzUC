% Task 6: ПИД с ZOH в обратной связи и задержкой τ=1.5 в прямой ветви.

clc; clear; close all;
load('W_cl.mat', 'W_cl');
W = W_cl;
s = tf('s');

% Подобранные параметры (см. task6_pid.py)
Kp = 0.2;
Ki = 0.35;
Kd = 0.0;
tau = 1.5;
Tzoh = 0.1;
setpoint_scale = 0.2;   % чтобы y_уст = 20 при x = 100

% ПИД с фильтром
N = 100;
C_pid = pid(Kp, Ki, Kd, 1/N);

% Задержка
G_delay = exp(-tau*s);
% pade-аппроксимация для tf
G_delay_pade = pade(G_delay, 3);

% Открытая система
L = C_pid * G_delay_pade * W;
% Прешкейл уставки + ОС
Cl = setpoint_scale * feedback(L, 1);

t = 0:0.005:30;
x = 100*ones(size(t));
y = lsim(Cl, x, t);
info = stepinfo(y, t, 20);

figure('Position',[100 100 1000 500]);
plot(t, y, 'LineWidth', 1.5); hold on; grid on;
yline(20, '--', 'y_{уст}=20');
yline(20*1.05, ':', '+5%');
yline(20*0.95, ':', '-5%');
yline(20*1.30, 'r:', 'σ=30%');
xlabel('t, с'); ylabel('y(t)');
title(sprintf('Task 6: ПИД K_p=%.2f K_i=%.2f K_d=%.2f, σ=%.2f%%, t_{пп}=%.2fс', ...
              Kp, Ki, Kd, info.Overshoot, info.SettlingTime));
saveas(gcf, 'task6_pid.png');
fprintf('y_уст=%.2f, σ=%.2f%%, t_пп=%.2fс\n', y(end), info.Overshoot, info.SettlingTime);
