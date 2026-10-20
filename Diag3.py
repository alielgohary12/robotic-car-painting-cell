from robodk import robolink
import re, struct

RDK = robolink.Robolink()
car = RDK.Item('Car_Body', robolink.ITEM_TYPE_OBJECT)
print("Car PoseAbs:\n", car.PoseAbs())

data = open(r"D:\RoboDK Tasks\car_final.stl", 'rb').read()
vs = [tuple(float(x) for x in m.groups())
      for m in re.finditer(rb'vertex\s+(\S+)\s+(\S+)\s+(\S+)', data)]
xs, ys, zs = zip(*vs)
print("car_final.stl Min:", round(min(xs),1), round(min(ys),1), round(min(zs),1))
print("car_final.stl Max:", round(max(xs),1), round(max(ys),1), round(max(zs),1))