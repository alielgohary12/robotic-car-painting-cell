from robodk import robolink, robomath as rm

RDK = robolink.Robolink()
car = RDK.Item('Car_Body', robolink.ITEM_TYPE_OBJECT)

pose = rm.transl(2438.35, -1259.55, -51.4) * rm.rotz(rm.pi/2)
car.setPose(pose)

print("Applied:\n", car.Pose())