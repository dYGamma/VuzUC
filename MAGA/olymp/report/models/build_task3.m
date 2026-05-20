function build_task3()
% Task 3: Simulink модель task3_model.slx с регулятором (П, K_p = 4) и объектом W
% Объект — замкнутая ПФ из Task 1. Загружается из W_cl.mat (нужно сначала запустить
% scripts/task1_reduce.m чтобы получить W_cl.mat).

mdl = 'task3_model';
close_system(mdl, 0);
new_system(mdl);
open_system(mdl);

% Параметры
Kp = 4;
% Числитель/знаменатель замкнутой ПФ из Task 1
num_W = [1181700000 24464220000 16604400000];
den_W = [3 9090062 187860040 23755200000 16604400000];

add_block('simulink/Sources/Step', [mdl '/Step'], ...
    'Time','0','Before','0','After','100', 'Position','[20 100 50 130]');
add_block('simulink/Math Operations/Sum', [mdl '/Sum'], ...
    'Inputs','+-','Position','[80 100 110 130]');
add_block('simulink/Math Operations/Gain', [mdl '/Kp'], ...
    'Gain', num2str(Kp), 'Position','[140 95 180 135]');
add_block('simulink/Continuous/Transfer Fcn', [mdl '/W'], ...
    'Numerator', mat2str(num_W), 'Denominator', mat2str(den_W), ...
    'Position','[210 90 320 140]');
add_block('simulink/Sinks/Scope', [mdl '/Scope'], 'Position','[360 95 390 135]');
add_block('simulink/Sinks/To Workspace', [mdl '/y_out'], ...
    'VariableName','y_log','Position','[360 150 400 180]');

add_line(mdl, 'Step/1','Sum/1');
add_line(mdl, 'Sum/1','Kp/1');
add_line(mdl, 'Kp/1','W/1');
add_line(mdl, 'W/1','Scope/1');
add_line(mdl, 'W/1','y_out/1','autorouting','on');
add_line(mdl, 'W/1','Sum/2','autorouting','on');

set_param(mdl, 'StopTime','15');
save_system(mdl);
fprintf('Сохранено: %s.slx\n', mdl);
end
