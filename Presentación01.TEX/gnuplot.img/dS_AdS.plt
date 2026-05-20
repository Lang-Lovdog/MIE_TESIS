## Gráfica del vacío de Sitter y Anti de Sitter ##
#set term wxt size 640,210

load palettefile("viridis")


set term epslatex input nobackground noheader size 12,4
set output "img/dS_AdS.tex"

set pm3d
set hidden3d
set isosamples 100

unset key
unset title
unset xtics
unset ytics
unset ztics
unset border
unset colorbox

set multiplot layout 1,3


## Anti de Sitter ##
set parametric
AdSX(u,v,r) = sqrt(r+u**2)*cos(v)
AdSY(u,v,r) = sqrt(r+u**2)*sin(v)
AdSZ(u,v,r) = u

a=1
b=1
c=8
r=8

set view 50,12
splot a*AdSX(u,v,r), b*AdSY(u,v,r), c*AdSZ(2*u,v,r)
unset parametric


## Mikovsky ##
set parametric
MkX(u,v) = u
MkY(u,v) = v
MkZ(u,v) = 0

set view 10,0
splot MkX(u,v), MkY(u,v), MkZ(u,v)

unset parametric

set parametric

## de Sitter ##

#Sphere parametric equation
dsX(u,v) = sin(u)*cos(v)
dsY(u,v) = sin(u)*sin(v)
dsZ(u,v) = cos(u)

set view 120,0
splot dsX(u,v), dsY(u,v), dsZ(u,v)

unset parametric

unset multiplot
