from robodk import robolink

RDK = robolink.Robolink()
car = RDK.Item('Car_Body', robolink.ITEM_TYPE_OBJECT)
frame = RDK.Item('Car_Frame', robolink.ITEM_TYPE_FRAME)

print("Car Pose (relative to frame):\n", car.Pose())
print("Car PoseAbs (in station):\n", car.PoseAbs())
print("Car GeometryPose:\n", car.GeometryPose())
print("Car_Frame PoseAbs:\n", frame.PoseAbs())