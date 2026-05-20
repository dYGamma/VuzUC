% Task 3: синтез линейного регулятора (рис.2)
% Требования: y_уст=80, σ≤30%, t_пп≤7с, x=100·1(t)

clc; clear; close all;
load('W_cl.mat', 'W_cl');
W = W_cl;   % объект — ПФ из Task 1

s = tf('s');
t = 0:0.001:15;
x = 100*ones(size(t));

% =================================================================
% Метод 1: П-регулятор по условию статики
% y_уст/x = Kp/(1+Kp) = 0.8 ⇒ Kp = 4
Kp1 = 4;
Cl1 = feedback(Kp1*W, 1);
y1 = lsim(Cl1, x, t);
info1 = stepinfo(y1, t, y1(end));
fprintf('М1 (П, Kp=%g): y_уст=%.2f, σ=%.2f%%, t_пп=%.3fс\n', ...
        Kp1, y1(end), info1.Overshoot, info1.SettlingTime);

% =================================================================
% Метод 2: ПД-регулятор Kp=4, Td=0.1
Kp2 = 4; Td = 0.1;
C2 = Kp2*(1 + Td*s);
Cl2 = feedback(C2*W, 1);
y2 = lsim(Cl2, x, t);
info2 = stepinfo(y2, t, y2(end));
fprintf('М2 (ПД, Kp=%g, Td=%g): y_уст=%.2f, σ=%.2f%%, t_пп=%.3fс\n', ...
        Kp2, Td, y2(end), info2.Overshoot, info2.SettlingTime);

% =================================================================
% Метод 3: предкомпенсатор + большой Kp
Kp3 = 20;
prescale = 0.8*(1+Kp3)/Kp3;
Cl3 = prescale*feedback(Kp3*W, 1);
y3 = lsim(Cl3, x, t);
info3 = stepinfo(y3, t, y3(end));
fprintf('М3 (Kp=%g + предкомп %.3f): y_уст=%.2f, σ=%.2f%%, t_пп=%.3fс\n', ...
        Kp3, prescale, y3(end), info3.Overshoot, info3.SettlingTime);

figure('Position',[100 100 1000 500]);
plot(t, y1, 'LineWidth', 1.4); hold on;
plot(t, y2, 'LineWidth', 1.4);
plot(t, y3, 'LineWidth', 1.4);
yline(80, '--', 'y_{уст}=80');
yline(80*1.3, ':', 'σ=30%');
grid on; xlabel('t, с'); ylabel('y(t)');
legend('М1: П, Kp=4', 'М2: ПД, Kp=4, Td=0.1', 'М3: K_p=20+предкомп', 'Location','southeast');
title('Task 3: переходные процессы для трёх методов');
saveas(gcf, 'task3_compare.png');
