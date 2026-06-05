### BACKGROUND ###
#set term wxt size 480,288 background rgb 'black'
set term png transparent truecolor size 960,864
set output 'Branes.png'
#set term epslatex input nobackground noheader size 5,3
#set output 'img/Branes.tex'

load palettefile("viridis")
#load palettefile("set1")

unset key
unset xtics
unset ytics
unset ztics
unset border

set isosamples 40, 40

set multiplot layout 2,1

set parametric

x(t) = 2 * cos(t)
y(t) = 2 * sin(t)
z(t) = 5 * sin(2*t)+20*cos(3*t/8)*sin(5*t)/4-14*sin(12*t)/5

set xrange [-2:2]

# Cuerda Abierta
set view 103,158
splot  [t=0:2*pi] x(0), v, z(t) \
, x(0),  y(0),    z(0) with points pointtype 7 pointsize 1.5 \
, x(t/2),y(t/4),  z(t/1.7) with lines lw 3 lc 3\
, x(pi), y(pi/2), z(2*pi/1.7) with points pointtype 7 pointsize 1.5 \
, x(pi), v, z(t)
unset parametric

set parametric

x(t) = 2 * cos(t)
y(t) = 2 * sin(t)
z(t) = 5 * sin(2*t)+20*cos(3*t/8)*sin(5*t)/4-14*sin(12*t)/5

set xrange [-2:2]

# Cuerda Abierta
set view 103,340
splot  [t=0:2*pi] x(pi), v, z(t) lc 5 \
, x(0),  y(0),    z(0) with points pointtype 7 pointsize 1.2 \
, x(t/2),y(t/4),  z(t/1.7) with lines lw 3 lc 3 \
, x(pi), y(pi/2), z(2*pi/1.7) with points pointtype 7 pointsize 1.5 \
, x(0), v, z(t) lc 1
unset parametric

unset multiplot

#!magick img/Branes.png -blur 0x1 img/Branes.png
