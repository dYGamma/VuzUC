function build_task1()
% Simulink модель task1_model.slx — структурная схема рис.1 (Task 1).
% На выходе scope y(t) — переходная характеристика всей замкнутой системы.

mdl = 'task1_model';
close_system(mdl, 0);
new_system(mdl);
open_system(mdl);

add_block('simulink/Sources/Step', [mdl '/Step'], ...
    'Time','0','Before','0','After','100', 'Position','[20 100 50 130]');
add_block('simulink/Math Operations/Sum', [mdl '/Sum1'], ...
    'Inputs','+-', 'Position','[80 100 110 130]');
add_block('simulink/Continuous/Transfer Fcn', [mdl '/W1'], ...
    'Numerator','[0.7]','Denominator','[1.5 1]', 'Position','[140 95 200 135]');
add_block('simulink/Math Operations/Sum', [mdl '/Sum_pp'], ...
    'Inputs','++','Position','[230 100 260 130]');
add_block('simulink/Math Operations/Sum', [mdl '/Sum_inner'], ...
    'Inputs','+-','Position','[280 100 310 130]');
add_block('simulink/Continuous/Transfer Fcn', [mdl '/W2'], ...
    'Numerator','[3030]','Denominator','[0.01 0]','Position','[330 95 390 135]');
add_block('simulink/Math Operations/Gain', [mdl '/W3'], ...
    'Gain','10','Position','[410 100 440 130]');
add_block('simulink/Continuous/Transfer Fcn', [mdl '/W4'], ...
    'Numerator','[1]','Denominator','[0.1 0]','Position','[460 95 520 135]');
add_block('simulink/Math Operations/Gain', [mdl '/K13'], ...
    'Gain','13','Position','[140 30 180 60]');
add_block('simulink/Continuous/Transfer Fcn', [mdl '/Hsens'], ...
    'Numerator','[1]','Denominator','[0.05 1]','Position','[280 170 340 210]','Orientation','left');
add_block('simulink/Sinks/Scope', [mdl '/Scope_y'], 'Position','[560 95 590 135]');

add_line(mdl, 'Step/1','Sum1/1');
add_line(mdl, 'Sum1/1','W1/1');
add_line(mdl, 'W1/1','Sum_pp/1');
add_line(mdl, 'K13/1','Sum_pp/2');
add_line(mdl, 'Sum_pp/1','Sum_inner/1');
add_line(mdl, 'Sum_inner/1','W2/1');
add_line(mdl, 'W2/1','W3/1');
add_line(mdl, 'W3/1','W4/1');
add_line(mdl, 'W3/1','Sum_inner/2','autorouting','on');
add_line(mdl, 'Sum1/1','K13/1','autorouting','on');
add_line(mdl, 'W4/1','Scope_y/1');
add_line(mdl, 'W4/1','Hsens/1','autorouting','on');
add_line(mdl, 'Hsens/1','Sum1/2','autorouting','on');

set_param(mdl, 'StopTime','30');
set_param(mdl, 'Solver','ode15s', 'MaxStep','0.01', 'RelTol','1e-6');
save_system(mdl);
fprintf('Сохранено: %s.slx\n', mdl);
end
