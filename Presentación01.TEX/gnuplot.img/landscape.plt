## El Landscape ##
## Different cubes with inscribed spheres ##

unset ztics
unset ytics
unset xtics
unset colorbox
unset border
unset key

set isosamples 80
set hidden3d

load palettefile("plasma")


#set term wxt size 640,640 background rgb 'black'
set term epslatex input nobackground noheader size 5,3
set output 'img/landscape.tex'

## Planes grid ##

set xrange [-4.2:4.2]
set yrange [-4.2:4.2]
set zrange [-2:1.5]

set urange[-4.2:4.2]
set vrange[-4.2:4.2]

set parametric

# Planes
plane(u,i,f) = (u>i && u<f)? u : NaN
# Sphere
sx(u,v,xi,r) = xi + r*sin(u)*cos(v)
sy(u,v,yi,r) = yi + r*sin(u)*sin(v)
sz(u,v,zi,r) = zi + r*cos(u)

a=-1
b=-0.6

set view 50, 45
splot \
       -1,  u, plane(v,a,b) w l lc 4, 1, u, plane(v,a,b) w l lc 4, \
        u, -1, plane(v,a,b) w l lc 4, u, 1, plane(v,a,b) w l lc 4, \
       -3,  u, plane(v,a,b) w l lc 4, 3, u, plane(v,a,b) w l lc 4, \
        u, -3, plane(v,a,b) w l lc 4, u, 3, plane(v,a,b) w l lc 4, \
        sx(u,v, 0,0.6), sy(u,v, 0,0.6), sz(u,v,-0.6,0.6) lc 'white', \
        sx(u,v, 2,0.6), sy(u,v, 2,0.6), sz(u,v,-0.5,0.2) lc 2, \
        sx(u,v,-2,0.6), sy(u,v, 2,0.6), sz(u,v,-0.5,0.8) lc 3, \
        sx(u,v, 2,0.6), sy(u,v,-2,0.6), sz(u,v,-0.5,0.3) lc 4, \
        sx(u,v,-2,0.6), sy(u,v,-2,0.6), sz(u,v,-0.5,0.4) lc 5, \
        sx(u,v, 0,0.7), sy(u,v, 2,0.6), sz(u,v,-0.4,0.6) lc 6, \
        sx(u,v, 2,0.3), sy(u,v, 0,0.6), sz(u,v,-0.3,0.6) lc 7, \
        sx(u,v, 0,0.6), sy(u,v,-2,0.7), sz(u,v,-0.4,0.6) lc 8, \
        sx(u,v,-2,0.8), sy(u,v, 0,0.6), sz(u,v,-0.3,0.6) lc 9



unset parametric
