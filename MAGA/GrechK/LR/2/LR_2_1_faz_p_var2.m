clear
close all
figure(1) 
hold on
t = [0 1]
for x0 = [-0.35:0.1:0.35]
    for dx0 = [-0.75:0.1:0.75]
        [t,x]=ode45(@dxdt1,t,[x0 dx0]); 
        plot(x(:,1),x(:,2))
    end
end
