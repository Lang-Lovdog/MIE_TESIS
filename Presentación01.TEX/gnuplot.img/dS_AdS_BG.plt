## Gráfica del vacío de Sitter y Anti de Sitter ##
#set term wxt size 620,640 background rgb "#000000"

load palettefile("bupu")


set term png truecolor enhanced transparent  size 680,620
set output "img/dS_AdS_BG.png"

set hidden3d
set isosamples 80

unset key
unset title
unset xtics
unset ytics
unset ztics
unset border
unset colorbox

## Anti de Sitter ##
set multiplot layout 1,3
set parametric
AdSX(u,v,r) = sqrt(r+u**2)*cos(v)
AdSY(u,v,r) = sqrt(r+u**2)*sin(v)
AdSZ(u,v,r) = u
## Mikovsky ##
set parametric
MkX(u,v) = u
MkY(u,v) = v
MkZ(u,v) = 0
## de Sitter ##
#Sphere parametric equation
dsX(u,v,r) = r*sin(u)*cos(v)
dsY(u,v,r) = r*sin(u)*sin(v)
dsZ(u,v,r) = r*cos(u)

set xrange [-8:8]
set yrange [-8:8]

a=1
b=1
c=8
r=1
d=2

set view 0,45
splot AdSX(  u,v,r), AdSY(  u,v,r), AdSZ(2*u,v,r) lc 1, \
       dsX(2*u,v,d),  dsY(2*u,v,d),  dsZ(2*u,v,d) lc 2, \
       MkX(  u,v),    MkY(  u,v),    MkZ(u,v)     lc 8

set view 58,45
splot AdSX(  u,v,r), AdSY(  u,v,r), AdSZ(2*u,v,r) lc 7, \
       dsX(2*u,v,d),  dsY(2*u,v,d),  dsZ(2*u,v,d) lc 5, \
       MkX(  u,v),    MkY(  u,v),    MkZ(u,v)     lc 3

set view 85,45
splot AdSX(  u,v,r), AdSY(  u,v,r), AdSZ(2*u,v,r) lc 4, \
       dsX(2*u,v,d),  dsY(2*u,v,d),  dsZ(2*u,v,d) lc 6, \
       MkX(  u,v),    MkY(  u,v),    MkZ(u,v)     lc 9

unset parametric
unset multiplot

!magick img/dS_AdS_BG.png -brightness-contrast -56x-10 -blur 2x15 img/dS_AdS_BG.png
