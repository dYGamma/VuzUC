% Task 5: нелинейный логический регулятор
% Структура: блоки с переключателями. Реализация — через MATLAB Function в Simulink.

clc; clear; close all;
load('W_cl.mat', 'W_cl');

% Демонстрация структуры регулятора:
%   F(e) реализуется как MATLAB Function-блок, содержащий внутренние
%   динамические ветви (2s+1)/(5s+1)e и (2s+1)/(3s+1)e и
%   18/(0.05s+1)·(2s+1)/(5s+1)e либо 5·(2s+1)/(3s+1)e
%
% Алгоритм:
%   delta = 1; k = 1;
%   if e > 10
%       lead = lead5_state          % выход (2s+1)/(5s+1)e
%   else
%       lead = lead3_state          % выход (2s+1)/(3s+1)e
%   end
%   if abs(lead) > 7
%       z = h18_state               % выход 18/(0.05s+1)·lead5_state
%   else
%       z = 5*lead3_state
%   end
%   if abs(z) <= delta
%       F = 0
%   else
%       F = k*z - delta*sign(z)
%   end

disp('Регулятор для Task 5 реализован в Simulink через MATLAB Function.');
disp('Динамические ветви (2s+1)/(5s+1) и (2s+1)/(3s+1) вынесены в отдельные');
disp('Transfer Fcn-блоки, их выходы передаются в MATLAB Function-блок.');
disp('См. модель task5_nlreg.slx');

% Параметры для модели
delta = 1.0;
k_gain = 1.0;
T_lead5 = 5; T_lead3 = 3;
T_h18 = 0.05; K_h18 = 18;
save('task5_params.mat', 'delta','k_gain','T_lead5','T_lead3','T_h18','K_h18');
