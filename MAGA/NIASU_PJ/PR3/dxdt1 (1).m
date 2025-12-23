%задание 1
function dx=dxdt1(t,x) 
dx=zeros(2,1);
dx(1)=-0.8*x(2);
dx(2)= -6*x(1)*x(2);
end

%задание 2
% function dx=dxdt1(t,x) 
% dx=zeros(2,1);
% dx(1)=-x(1)^3+x(1)*x(2);
% dx(2)= -x(2)^3-x(1)^2;
% end
