% Task 4: аппроксимация нелинейной характеристики F(e)

clc; clear; close all;

% Точки
e_data = [-50 -45 -30 -20 0 20 30 45 50];
F_data = [2.85 2 1.7 1.4 0 1.4 1.7 2 2.85];

% (1) кусочно-линейная — через interp1
F_pwl = @(e) interp1(e_data, F_data, e, 'linear', 'extrap');

% (2) полином 3-й ст. по |e|
abs_e = abs(e_data);
p = polyfit(abs_e, F_data, 3);
F_poly = @(e) polyval(p, abs(e));
fprintf('Полином 3-й ст.: %+.4e|e|^3 %+.4e|e|^2 %+.4e|e| %+.4f\n', p(1),p(2),p(3),p(4));

% (3) степенная F = a·|e|^b
mask = abs_e > 0;
P = polyfit(log(abs_e(mask)), log(F_data(mask)), 1);
b = P(1); a = exp(P(2));
F_pow = @(e) a*abs(e).^b;
fprintf('Степенная: F = %.4f·|e|^%.4f\n', a, b);

% Построение
e_grid = linspace(-60, 60, 1201);
figure('Position',[100 100 900 500]);
plot(e_data, F_data, 'ko', 'MarkerSize',8, 'MarkerFaceColor','k'); hold on;
plot(e_grid, F_pwl(e_grid), 'LineWidth', 1.5);
plot(e_grid, F_poly(e_grid), '--', 'LineWidth', 1.5);
plot(e_grid, F_pow(e_grid), ':', 'LineWidth', 2);
grid on; xlabel('e'); ylabel('F(e)');
legend('Точки', 'Кусочно-линейная', 'Полином 3 ст.', 'Степенная','Location','south');
title('Task 4: аппроксимации F(e)');
saveas(gcf, 'task4_approx.png');

% Моделирование (Simulink): импорт W из Task 1, нелинейный блок (Lookup, MATLAB Fcn)
% Здесь — м-скрипт для генерации Lookup Table:
breakpoints = [-60 -55 e_data 55 60];   % с экстраполяцией
table_pwl = [interp1(e_data, F_data, [-60 -55], 'linear', 'extrap') ...
             F_data ...
             interp1(e_data, F_data, [55 60], 'linear', 'extrap')];
save('task4_lookup.mat', 'breakpoints', 'table_pwl', 'p', 'a', 'b');
disp('Данные для Simulink (Lookup) сохранены в task4_lookup.mat');
