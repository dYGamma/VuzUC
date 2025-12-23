clear
clc
syms x_1 x_2

eqns = [-x_2-2*x_1==0, 1-x_1-x_2*(1-0.5*x_1^2)==0]; %var15

S1 = solve(eqns,[x_1 x_2], 'maxdegree', 6);

x1x2_1=[round(S1.x_1(1),3) round(S1.x_2(1),3)]
x1x2_2=[round(S1.x_1(2),3) round(S1.x_2(2),3)]
x1x2_3=[round(S1.x_1(3),3) round(S1.x_2(3),3)]


x1 = 1.325;
x2 = -2.649;

J = [-2 -1;-1+x1*x2 -1+0.5*x1^2]; %var15

syms m 

J_1 = J-[m 0; 0 m];

eqn = det(J_1);
S = solve(eqn,m);

k1 = round(S(1),3)
k2 = round(S(2),3)

