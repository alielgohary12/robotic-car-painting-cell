from robodk import robolink, robomath as rm
import os, re, struct

RDK = robolink.Robolink()
car = RDK.Item('Car_Body', robolink.ITEM_TYPE_OBJECT)

# Put the car back at the frame origin, no rotation
car.setPose(rm.eye(4))

path = os.path.join(r"D:\RoboDK Tasks", "car_reset.stl")
car.Save(path)

data = open(path, 'rb').read()
pts = []
if data[:80].lstrip().lower().startswith(b'solid') and b'facet' in data[:2000].lower():
    for m in re.finditer(rb'vertex\s+(\S+)\s+(\S+)\s+(\S+)', data):
        pts.append(tuple(float(x) for x in m.groups()))
else:
    n = struct.unpack('<I', data[80:84])[0]
    off = 84
    for _ in range(n):
        v = struct.unpack('<12fH', data[off:off+50])
        pts += [v[3:6], v[6:9], v[9:12]]
        off += 50

xs, ys, zs = zip(*pts)
print("Min:", round(min(xs),1), round(min(ys),1), round(min(zs),1))
print("Max:", round(max(xs),1), round(max(ys),1), round(max(zs),1))
print("Size:", round(max(xs)-min(xs),1), round(max(ys)-min(ys),1), round(max(zs)-min(zs),1))