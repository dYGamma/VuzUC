function dx=dxdt1(t,x) 
dx=zeros(2,1);
dx(1)=x(2);
dx(2)= 2*sign(-x(1));
end