clear
clc
syms A w


eqns = [w==20/(pi*A^2), A*w^2-10*A==(80/pi)*sqrt(1-(0.5/A)^2)];

%eqns = [(200-20*w^2)/(w^4-16*w^2+100) == (-pi*A^2*sqrt(4*A^2-1))/(8*A^2+6), (-40*w)/(w^4-16*w^2+100) == (-2*pi*A^2)/(8*A^2+6)];

%  eqns = [(200-20*w^2)/(w^4-16*w^2+100) == -(pi/2)*sqrt(4*A^2-1), (-40*w)/(w^4-16*w^2+100) == -pi];

S1 = solve(eqns,[w A], 'maxdegree', 6);

w1A1=[round(S1.w(1),3) round(S1.A(1),2)]
w2A2=[round(S1.w(2),3) round(S1.A(2),2)]
w3A3=[round(S1.w(3),3) round(S1.A(3),2)]
w4A4=[round(S1.w(4),3) round(S1.A(4),2)]
w5A5=[round(S1.w(5),3) round(S1.A(5),2)]
w6A6=[round(S1.w(6),3) round(S1.A(6),2)]
w7A7=[round(S1.w(7),3) round(S1.A(7),2)]
w8A8=[round(S1.w(8),3) round(S1.A(8),2)]