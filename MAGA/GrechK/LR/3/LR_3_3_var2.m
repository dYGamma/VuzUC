clc
clear
close all
W=zpk([-10 -10],[-1 -1 -1],1); 
nyquist(W); 
A=0:0.001:10; 
k=0.5;
delta = 0.5;
N=(2*k/pi)*(asin(delta./A)+(delta./A).*sqrt(1-(delta./A).^2));
N1=-1./N;
hold on 
plot(real(N1),imag(N1)); 
axis([-3 0 -0.5 2])