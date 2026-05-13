clc
clear
close all
W=zpk([-10 -10],[-1 -1 -1],1); 
nyquist(W); 
A=0:0.001:1; 
k=1.5;
N=(4*k)./(pi.*A);
N1=-1./N;
hold on 
plot(real(N1),imag(N1)); 
 axis([-5 0 -0.2 0.2])
 
%  clc
% clear
% close all
% W=zpk([-10 -10],[-1 -1 -1],1); 
% nyquist(1/W); 
% A=0:0.001:10; 
% k=1.5;
% N=(4*k)./(pi.*A);
% N1=-1./N;
% hold on 
% plot(real(N),imag(N)); 
%  axis([-5 0 -0.2 0.2])