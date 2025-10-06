### BACKGROUND ###
#set term wxt size 480,288 background rgb 'black'
set term png transparent truecolor size 480,288
set output 'img/VibratingStringsBackground.png'

load palettefile("magma")

unset key
unset xtics
unset ytics
unset border

set multiplot layout 3,1

plot [t=0:4*pi] sin(t)  ,  sin(-t)
plot [t=0:4*pi] sin(2*t),  sin(-2*t)
plot [t=0:4*pi] sin(3*t),  sin(-3*t)

unset multiplot

!magick img/VibratingStringsBackground.png -blur 0x4 -brightness-contrast -12x-5 img/VibratingStringsBackground.png


### Strings ###
#set term wxt size 480,96 background rgb 'black'
#set term png transparent truecolor size 960,192
#set output 'img/VibratingStrings.tex'
set term epslatex input nobackground noheader size 12,5
set output 'img/VibratingStrings.tex'

#load palettefile("sand")
load palettefile("rdpu")

unset key
unset xtics
unset ytics
unset border


set multiplot layout 2,3
plot [t=0:2*pi] sin(   t) lw 2
plot [t=0:2*pi] (t<7*pi/8)? sin(-2*t) : NaN lw 2, (t>pi)? sin(-2*t):NaN lw 2
plot [t=0:2*pi] sin( 3*t) lw 2
#unset multiplot

#!magick img/VibratingStrings.png -blur 0x1 img/VibratingStrings.png

### CLOSED STRINGS ###
#set term wxt size 480,192 background rgb 'black'
#set term png transparent truecolor size 960,192
#set output 'img/VibratingStringsClosed.png'
#set term epslatex input nobackground noheader size 12,3
#set output 'img/VibratingStringsClosed.tex'

load palettefile("sand")

unset key
unset xtics
unset ytics
unset ztics
unset border

# Define the parametric equations
set parametric
x(t) = 2 * cos(t)
y(t) = 2 * sin(t)
z(t) = sin(2*t)

# Plot the ring perimeter
#set multiplot layout 1,3
set view 45,20
splot [t=0:2*pi] x(t), y(t), z(t) with lines lw 2

set view 15,30
splot [t=0:2*pi] x(t), y(t), z(t) with lines lw 2

set view 50,73
splot [t=0:2*pi] x(t), y(t), 2*z(1.5*t) with lines lw 2

unset multiplot
unset parametric

#!magick img/VibratingStringsClosed.png -blur 0x1 img/VibratingStringsClosed.png
