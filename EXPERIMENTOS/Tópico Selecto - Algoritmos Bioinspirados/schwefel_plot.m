x1 = -500:10:500;
x2 = -500:10:500;

### plot 3d for x1,x2 and f(x1,x2)

f = zeros(length(x1),length(x2));
for i = 1:length(x1)
    for j = 1:length(x2)
        f(i,j) = schwefel(x1(i),x2(j));
    end
end

surf(x1,x2,f)
hold on
xMin= 420.9687;
plot3(xMin, xMin, schwefel(xMin, xMin), 'ro')
