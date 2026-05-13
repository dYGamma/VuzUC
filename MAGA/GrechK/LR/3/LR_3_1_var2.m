clc
clear
close all
W=tf(20,[1 2 10]); 
nyquist(W); 
A=0:0.001:100; 
k=0.5;
delta = 0.5;
N=((4*k)./(pi.*A)).*(sqrt(1-(delta./A).^2)-j*(delta./A)); 
N1=-1./N;
hold on 
plot(real(N1),imag(N1)); 