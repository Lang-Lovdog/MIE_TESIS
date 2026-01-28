## World lines and world sheets ##

unset colorbox
unset key
unset title
unset xtics
unset ytics
unset ztics
set hidden3d
set isosamples 60

set term wxt enhanced
#set term epslatex input nobackground notitle size 6,4
#set output 'WorldLinesAndWorldSheets.tex'

#set multiplot layout 1,2
set ylabel 'space'
set zlabel 'time'
set view 70,85
set xrange [-3:3]
set yrange [-3:3]
set zrange [-1.5:1.5]

## World lines ##
set parametric
glx(u,v) = 0.3*cos(0.75*v)*sin(0.5*v)*cos(9*v)
gly(u,v) = 0.3*cos(0.75*v)*sin(2*v)*sin(3.9*v)
glz(u,v) = v
splot glx(u,v), gly(u,v), glz(u,v) lw 2
unset parametric

#### World sheets ##
##set parametric
##gcx(u,v) = cos(u)+glx(u,v)
##gcy(u,v) = 2*sin(u)+gly(u,v)
##gcz(u,v) = v
##splot gcx(u,v), gcy(u,v), gcz(u,v)
##unset parametric

#unset multiplot
