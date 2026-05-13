clc
clear
close all
W=tf(0.3,[0.0001 0.0401 0.13 0]); 
nyquist(W); 
A=0:0.001:10; 
N=96./(pi.*A); 
N1=-1./N;
hold on 
plot(real(N1),imag(N1)); 
axis([-0.02 0.02 -0.0003 0.0003])