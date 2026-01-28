## World lines and world sheets ##

unset colorbox
unset key
unset title
unset xtics
unset ytics
unset ztics
set isosamples 40
set hidden3d
set tics font "VictorMono Nerd Font Mono,9"
set border ls 50
#set tics textcolor rgb "#ffccff"

load palettefile("sand")

#set term wxt enhanced background rgb "#000000"
set term epslatex input nobackground noheader size 6,4
set output 'img/WorldLinesAndWorldSheets.tex'

set multiplot layout 1,2
set ylabel 'space'
set zlabel 'time'
set view 70,85
set xrange [-2:2]
set yrange [-2:2]
set zrange [-1.5:1.5]

## World lines ##
set parametric
lx(u,v) = 0.2*cos(0.75*v)*sin(0.5*v)*cos(9*v)
ly(u,v) = 0.2*cos(0.75*v)*sin(2*v)*sin(3.9*v)
lz(u,v) = v
## World sheets ##
cx(u,v,r) = r*cos(u)+lx(u,v)
cy(u,v,r) = r*sin(u)+ly(u,v)
cz(u,v)   = v

a=-1.5

splot cx(u,v,0.03), cy(u,v,0.03), cz(u,v),  \
      cx(u,a,0.03), cy(u,a,0.03), cz(u,a),  \
      cx(u,a,0.05), cy(u,a,0.05), cz(u,a)
splot cx(u,v,1.2 ), cy(u,v,1.2 ), cz(u,v),  \
      cx(u,v,1.2 ), cy(u,v,1.2 ), cz(u,a)

unset parametric

unset multiplot
