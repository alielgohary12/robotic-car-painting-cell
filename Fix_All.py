from robodk import robolink, robomath as rm

RDK = robolink.Robolink()
car = RDK.Item('Car_Body', robolink.ITEM_TYPE_OBJECT)
robot = RDK.Item('ABB IRB 6700-235/2.65', robolink.ITEM_TYPE_ROBOT)

# 1) Reset the robot base to the station origin (no tilt, no rotation)
robot.Parent().setPose(rm.eye(4))   # robot's base frame

# 2) Place the car: center -> origin, then rotate 90 deg, then lift
pose = rm.transl(0, 0, -51.4) * rm.rotz(rm.pi/2) * rm.transl(-1259.55, -2438.35, 0)
car.setPose(pose)

print("Robot base now:\n", robot.Parent().Pose())
print("Car pose:\n", car.Pose())