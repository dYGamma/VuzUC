%1 задание
% clear
% close all
% figure(1) 
% hold on
% t = [0 2]
% for x0 = -1.5:0.1:1.5
%     for dx0 = -1.5:0.1:1.5
%         [t,x]=ode45(@dxdt1,t,[x0 dx0]); 
%         plot(x(:,1),x(:,2))
%     end
% end

%2 задание
clear
close all
figure(1) 
hold on
t = [0 2]
for x0 = -1.5:0.1:1.8
    for dx0 = -3.5:0.1:1.5
        [t,x]=ode45(@dxdt1,t,[x0 dx0]); 
        plot(x(:,1),x(:,2))
    end
end
