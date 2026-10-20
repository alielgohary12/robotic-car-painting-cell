from robodk import robolink, robomath
import os

RDK = robolink.Robolink()
station = RDK.ActiveStation()

def make_box(name, sx, sy, sz, x, y, z, color=None):
    # Create a box via a temporary STL file, then place it in the station
    path = os.path.join(os.environ.get('TEMP', '.'), name + '.stl')
    hx, hy, hz = sx/2, sy/2, sz/2
    v = [(-hx,-hy,-hz),(hx,-hy,-hz),(hx,hy,-hz),(-hx,hy,-hz),
         (-hx,-hy,hz),(hx,-hy,hz),(hx,hy,hz),(-hx,hy,hz)]
    f = [(0,2,1),(0,3,2),(4,5,6),(4,6,7),(0,1,5),(0,5,4),
         (2,3,7),(2,7,6),(1,2,6),(1,6,5),(3,0,4),(3,4,7)]
    with open(path, 'w') as fh:
        fh.write('solid %s\n' % name)
        for a, b, c in f:
            fh.write('facet normal 0 0 0\nouter loop\n')
            for i in (a, b, c):
                fh.write('vertex %f %f %f\n' % v[i])
            fh.write('endloop\nendfacet\n')
        fh.write('endsolid\n')
    item = RDK.AddFile(path)
    item.setName(name)
    item.setPose(robomath.transl(x, y, z))
    if color:
        item.Recolor(color)
    return item

# Floor 12000 x 8000 x 100, top surface at Z=0
make_box('Floor', 12000, 8000, 100, 0, 0, -50, [0.6, 0.6, 0.6, 1])
# Back wall 12000 x 100 x 4000
make_box('Wall_Back', 12000, 100, 4000, 0, -4050, 2000, [0.8, 0.8, 0.9, 0.4])
# Side wall 100 x 8000 x 4000
make_box('Wall_Side', 100, 8000, 4000, -6050, 0, 2000, [0.8, 0.8, 0.9, 0.4])

print("Done: Floor + walls created")