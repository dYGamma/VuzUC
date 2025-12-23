close all
w=-100:0.1:100;
W=((18*(j*w)-5)./(9*(j*w).^2+(j*w)-91)).*(1./(5*j*w));
Um=real(W);
Vm=imag(W);
Vm1=imag(W).*w;
plot(Um,Vm); hold;
plot(Um,Vm1);
grid;
xlabel('U')
ylabel('jVU')
legend('АФХ','Мод АФХ')