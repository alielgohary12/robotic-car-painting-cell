from robodk import robolink
import os, re, struct

RDK = robolink.Robolink()
car = RDK.Item('Car_Body', robolink.ITEM_TYPE_OBJECT)
robot = RDK.Item('ABB IRB 6700-235/2.65', robolink.ITEM_TYPE_ROBOT)

# Save with the current pose baked in, then read the real bounding box
path = r"D:\RoboDK Tasks\car_now.stl"
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
print("Car pose in station:", car.PoseAbs())
print("Robot base in station:", robot.PoseAbs())
print("Min:", round(min(xs),1), round(min(ys),1), round(min(zs),1))
print("Max:", round(max(xs),1), round(max(ys),1), round(max(zs),1))