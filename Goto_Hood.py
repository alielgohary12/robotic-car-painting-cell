from robodk import robolink, robomath as rm

RDK = robolink.Robolink()
robot = RDK.Item('ABB IRB 6700-235/2.65', robolink.ITEM_TYPE_ROBOT)
frame = RDK.Item('Car_Frame', robolink.ITEM_TYPE_FRAME)
tool  = RDK.Item('Generic Paint Sprayer', robolink.ITEM_TYPE_TOOL)

robot.setPoseFrame(frame)
robot.setPoseTool(tool)
robot.setJoints(robot.JointsHome())

# Gun pointing down, in Car_Frame, for the TCP
target = rm.transl(1000, 0, 1500) * rm.rotx(rm.pi)

try:
    robot.MoveJ(target)          # solves IK with the active frame and tool
    print("OK. Pose now:", robot.Pose())
except Exception as e:
    print("NOT REACHABLE:", e)