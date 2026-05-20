function y = aim2(u, t)
    % АИМ-2: блок MATLAB Function для Simulink.
    % Вход:  u — текущее значение непрерывного сигнала
    %        t — текущее время (берётся блоком Clock в Simulink)
    % Выход: y — выходной квантованный сигнал
    T = 1.0;
    gamma = 0.6;
    phase = mod(t, T);
    if phase < gamma*T
        y = u;
    else
        y = 0;
    end
end
