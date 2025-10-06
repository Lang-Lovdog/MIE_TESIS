### STRINGS INTERACTIONS ###
#set term wxt size 640,576 background rgb 'black'
#set term png transparent truecolor size 960,864
#set output 'img/StringsInteractions.png'
set term epslatex input nobackground noheader size 7,4
set output 'img/StringsInteractions.tex'

load palettefile("set2")

unset key
unset xtics
unset ytics
unset ztics
unset border

set style line 1 linewidth 2
set style line 2 linewidth 2

# Define the parametric equations
set multiplot layout 3,3
set parametric
x(t) = 2 * cos(t)
y(t) = 2 * sin(t)
z(t) = 5*sin(2*t)+20*cos(3*t/8)*sin(5*t)/4-14*sin(12*t)/5

c(t) = (t<3*pi/7)? x(3*pi/7) : (t<6*pi/7)? x(t) : x(6*pi/7)
u(t) = (t<3*pi/7)? y(3*pi/7) : (t<6*pi/7)? y(t) : y(6*pi/7)
v(t) = sin(20*t)+30*cos(7*t)

# Cuerda Abierta
set view 130,180
splot [t=0:2*pi] x(t/9), y(t), z(t/1.7) with lines

# Cuerda cerrándose
set view 234,100
  splot [t=0:2*pi] c(t), y(t), (t<5*pi/7)? z(t) : v(t/3) with lines

# Cuerda cerrada
set view 33,75
splot [t=0:2*pi] [-3:3] [-3:3] [-3:3] x(t), y(t), z(t) with lines, 2.3+y(t/12), x(t/2)*3-2.3, v(t/3)/3-5 with lines
unset parametric

set parametric
x(t,d) = d+t**2
c(t,d) =-x(t,d)
v(t,d) = (t>0)? c(t,d) : x(t,d)
y(t) = t
u(t) = y(t)**2
z(t) = 3*sin(t)*cos(6*t/9)


# Cuerdas cercanas
set view 343,24
splot [t=-pi:pi] x(t,4), y(t), z(t) with lines, c(t,4), y(t), z(t) with lines

# Cuerdas se tocan
set view 343,24
splot [t=-pi:pi] x(t,0.4), y(t), z(t) with lines, c(t,0.4), y(t), z(t) with lines

# Cuerdas se tocan
set view 14,24
splot [t=-pi:pi] v(t,0.4), u(t)+3, z(t) with lines, v(t,0.4), -u(t)-3, z(t) with lines

unset parametric

set parametric

x(t) = 2 * cos(t)
c(t) = 2 * cos(t/2)
y(t) = 2 * sin(t)
z(t) = 5*sin(2*t)+20*cos(3*t)*sin(5*t)/4-14*sin(12*t)/5

set view 13,62
splot [t=0:2*pi] x(t), y(t), z(t) with lines

set view 5,122
splot [t=-pi/2:3*pi/2] x(t), y(2*t), z(t) with lines

set view 20,62
splot [t=-pi/2:3*pi/2] x(t), y(t)+2, z(t)-4 with lines, x(t), y(t)-4, z(t)+4 with lines
unset parametric



unset multiplot

#!magick img/StringsInteractions.png -blur 0x1 img/StringsInteractions.png
