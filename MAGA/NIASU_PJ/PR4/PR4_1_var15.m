close all
w=-500:0.1:500;
W=((18*(j*w)-5)./(9*(j*w).^2+(j*w)-91));
Um=real(W);
Vm=imag(W);
Vm1=imag(W).*w;
plot(Um,Vm); hold;
plot(Um,Vm1);
grid;
xlabel('U')
ylabel('jVU')
legend('АФХ','Мод АФХ')