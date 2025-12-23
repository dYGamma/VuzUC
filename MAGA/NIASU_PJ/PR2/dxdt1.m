% 1 задание
% function dx=dxdt1(t,x) 
% dx=zeros(2,1);
% dx(1)=-x(2);
% dx(2)= -x(1)^5-3*x(2)+x(1)*x(2);
% end

%2 задание
function dx=dxdt1(t,x) 
dx=zeros(2,1);
dx(1)=-x(2)-2*x(1);
dx(2)= 1-x(1)-x(2)*(1-0.5*x(1)^2);
end
