% Task 2: установившаяся ошибка при x = 100·1(t)

clc; clear; close all;
load('W_cl.mat', 'W_forward');

s = tf('s');
H  = 1/(0.05*s + 1);
W_open = W_forward * H;

% Аналитика: e_уст = lim_{s->0} s·X(s)/(1+W_open) при X(s)=100/s
% В W_open присутствует свободный интегратор ⇒ W_open(0) = ∞ ⇒ e_уст = 0
fprintf('W_open(0) = %g\n', dcgain(W_open));
fprintf('Поскольку в петле есть интегратор, e_уст = 100/(1+∞) = 0\n');

% Моделирование
t = 0:0.01:20;
x = 100*ones(size(t));

% Φ_e(s) = 1/(1 + W_open(s))
Phi_e = 1/(1 + W_open);
e_sim = lsim(Phi_e, x, t);

figure('Position',[100 100 900 450]);
plot(t, e_sim, 'LineWidth', 1.5); hold on; grid on;
yline(0, 'k--');
xlabel('t, с'); ylabel('e(t)');
title('Task 2: переходный процесс ошибки e(t) при x = 100·1(t)');
saveas(gcf, 'task2_error.png');

fprintf('e_уст (моделирование) = %.4e\n', e_sim(end));
