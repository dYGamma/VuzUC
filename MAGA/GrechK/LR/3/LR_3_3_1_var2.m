clear
clc
syms A


eqns = (2*0.5*1.99/pi)*(asin(0.5*A)+0.5/A*sqrt(1-(0.5/A)^2))==1;

S1 = solve(eqns,A, 'maxdegree', 6);
