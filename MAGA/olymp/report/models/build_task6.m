function build_task6()
% Task 6: ПИД с задержкой 1.5с в прямой ветви и ZOH в обратной связи.

mdl = 'task6_model';
close_system(mdl, 0);
new_system(mdl);
open_system(mdl);

% Параметры
Kp = 0.2;
Ki = 0.35;
Kd = 0;
tau = 1.5;
Tzoh = 0.1;
setpoint_scale = 0.2;
num_W = [1181700000 24464220000 16604400000];
den_W = [3 9090062 187860040 23755200000 16604400000];

add_block('simulink/Sources/Step', [mdl '/Step'], ...
    'Time','0','Before','0','After','100', 'Position','[20 130 50 160]');
add_block('simulink/Math Operations/Gain', [mdl '/Scale'], ...
    'Gain', num2str(setpoint_scale), 'Position','[80 130 110 160]');
add_block('simulink/Math Operations/Sum', [mdl '/Sum'], ...
    'Inputs','+-','Position','[140 130 170 160]');
add_block('simulink/Continuous/PID Controller', [mdl '/PID'], ...
    'P', num2str(Kp), 'I', num2str(Ki), 'D', num2str(Kd), ...
    'Position','[200 120 280 170]');
add_block('simulink/Continuous/Transport Delay', [mdl '/Delay'], ...
    'DelayTime', num2str(tau), 'Position','[310 130 370 160]');
add_block('simulink/Continuous/Transfer Fcn', [mdl '/W'], ...
    'Numerator', mat2str(num_W), 'Denominator', mat2str(den_W), ...
    'Position','[400 120 510 170]');
add_block('simulink/Discrete/Zero-Order Hold', [mdl '/ZOH'], ...
    'SampleTime', num2str(Tzoh), 'Position','[400 200 460 240]','Orientation','left');
add_block('simulink/Sinks/Scope', [mdl '/Scope'], 'Position','[550 125 580 165]');

add_line(mdl, 'Step/1','Scale/1');
add_line(mdl, 'Scale/1','Sum/1');
add_line(mdl, 'Sum/1','PID/1');
add_line(mdl, 'PID/1','Delay/1');
add_line(mdl, 'Delay/1','W/1');
add_line(mdl, 'W/1','Scope/1');
add_line(mdl, 'W/1','ZOH/1','autorouting','on');
add_line(mdl, 'ZOH/1','Sum/2','autorouting','on');

set_param(mdl, 'StopTime','40');
save_system(mdl);
fprintf('Сохранено: %s.slx\n', mdl);
end
