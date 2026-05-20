function build_task4()
% Task 4: Simulink модель task4_model.slx — три параллельных тракта с разной
% аппроксимацией F(e), один объект, переключение Manual Switch для выбора аппр.

mdl = 'task4_model';
close_system(mdl, 0);
new_system(mdl);
open_system(mdl);

% Объект (замкнутая ПФ из Task 1)
num_W = [1181700000 24464220000 16604400000];
den_W = [3 9090062 187860040 23755200000 16604400000];

% Точки таблицы
e_data = [-50 -45 -30 -20 0 20 30 45 50];
F_data = [2.85 2 1.7 1.4 0 1.4 1.7 2 2.85];

% Коэффициенты полинома 3-й степени по |e| (см. scripts/task4_approx.m)
% F(e) = p1*|e|^3 + p2*|e|^2 + p3*|e| + p4
p_coef = polyfit(abs(e_data), F_data, 3);
% Степенная: F = a*|e|^b (только ненулевые точки)
abs_e = abs(e_data);
mask = abs_e > 0;
ab = polyfit(log(abs_e(mask)), log(F_data(mask)), 1);
a_pow = exp(ab(2)); b_pow = ab(1);

% Блоки
add_block('simulink/Sources/Step', [mdl '/Step'], ...
    'Time','0','Before','0','After','100', 'Position','[20 100 50 130]');
add_block('simulink/Math Operations/Sum', [mdl '/Sum'], ...
    'Inputs','+-','Position','[80 100 110 130]');

% Кусочно-линейная — Lookup Table
add_block('simulink/Lookup Tables/1-D Lookup Table', [mdl '/F_pwl'], ...
    'BreakpointsForDimension1', mat2str(e_data), ...
    'Table', mat2str(F_data), ...
    'Position','[150 30 220 70]');

% Полиномиальная — через Fcn-блок
add_block('simulink/User-Defined Functions/Fcn', [mdl '/F_poly'], ...
    'Expr', sprintf('%g*abs(u)^3 + %g*abs(u)^2 + %g*abs(u) + %g', ...
                    p_coef(1), p_coef(2), p_coef(3), p_coef(4)), ...
    'Position','[150 90 220 130]');

% Степенная — через Fcn-блок
add_block('simulink/User-Defined Functions/Fcn', [mdl '/F_pow'], ...
    'Expr', sprintf('%g*abs(u)^%g', a_pow, b_pow), ...
    'Position','[150 150 220 190]');

% Manual Switch для выбора аппроксимации
add_block('simulink/Signal Routing/Multiport Switch', [mdl '/Sw'], ...
    'Inputs','3', 'Position','[250 80 280 200]');
add_block('simulink/Sources/Constant', [mdl '/Sel'], ...
    'Value','1', 'Position','[200 220 230 250]');

% Объект
add_block('simulink/Continuous/Transfer Fcn', [mdl '/W'], ...
    'Numerator', mat2str(num_W), 'Denominator', mat2str(den_W), ...
    'Position','[320 90 430 140]');
add_block('simulink/Sinks/Scope', [mdl '/Scope'], 'Position','[470 95 500 135]');

add_line(mdl, 'Step/1','Sum/1');
add_line(mdl, 'Sum/1','F_pwl/1','autorouting','on');
add_line(mdl, 'Sum/1','F_poly/1','autorouting','on');
add_line(mdl, 'Sum/1','F_pow/1','autorouting','on');
add_line(mdl, 'Sel/1','Sw/1');
add_line(mdl, 'F_pwl/1','Sw/2','autorouting','on');
add_line(mdl, 'F_poly/1','Sw/3','autorouting','on');
add_line(mdl, 'F_pow/1','Sw/4','autorouting','on');
add_line(mdl, 'Sw/1','W/1');
add_line(mdl, 'W/1','Scope/1');
add_line(mdl, 'W/1','Sum/2','autorouting','on');

set_param(mdl, 'StopTime','8');
save_system(mdl);
fprintf('Сохранено: %s.slx — Sel=1 (PWL), 2 (poly), 3 (pow)\n', mdl);
end
