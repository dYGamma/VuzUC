% Task 7: АИМ-2 (амплитудно-импульсный модулятор 2-рода)
% Реализация в Simulink через MATLAB Function блок.

clc; clear; close all;

% Содержимое блока MATLAB Function в Simulink:
%
% function y = aim2(u, t)
%     T = 1.0;        % период прерывания
%     gamma = 0.6;    % коэффициент скважности
%     phase = mod(t, T);
%     if phase < gamma*T
%         y = u;
%     else
%         y = 0;
%     end
% end
%
% Вход: u — мгновенное значение непрерывного сигнала, t — текущее время.
% Выход: y — выходной (квантованный) сигнал АИМ-2.

% Параллельная демонстрация на чистом MATLAB:
T = 1.0;
gamma = 0.6;
freq = 0.3;     % Hz

t = 0:0.001:10;
x = sin(2*pi*freq*t);

phase = mod(t, T);
y = x;
y(phase >= gamma*T) = 0;

figure('Position',[100 100 1100 450]);
plot(t, x, '--', 'Color',[.5 .5 .5], 'LineWidth',1); hold on;
plot(t, y, 'LineWidth', 1.4);
grid on; xlabel('t, с'); ylabel('сигнал');
legend('x(t)', 'x*(t) — выход АИМ-2', 'Location','northeast');
title(sprintf('Task 7: АИМ-2, T=%g с, γ=%.0f%%', T, gamma*100));
saveas(gcf, 'task7_aim2.png');

disp('MATLAB Function-блок для Simulink — см. файл task7_aim2_fcn.m');
