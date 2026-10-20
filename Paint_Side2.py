from robodk import robolink, robomath as rm

RDK = robolink.Robolink()
robot = RDK.Item('ABB IRB 6700-235/2.65', robolink.ITEM_TYPE_ROBOT)
frame = RDK.Item('Car_Frame', robolink.ITEM_TYPE_FRAME)
tool  = RDK.Item('Generic Paint Sprayer', robolink.ITEM_TYPE_TOOL)

print("robot valid:", robot.Valid(), "| frame valid:", frame.Valid(), "| tool valid:", tool.Valid())

robot.setPoseFrame(frame)
robot.setPoseTool(tool)

# Current gun pose in Car_Frame (a pose the robot can actually reach)
base_pose = robot.Pose()
print("Start pose:", base_pose)

def shifted(dx, dz):
    # same orientation, shifted along Car_Frame X and Z
    return rm.transl(dx, 0, dz) * base_pose

targets = []
for i, dz in enumerate([-150, -50, 50, 150]):
    if i % 2 == 0:
        targets += [shifted(-400, dz), shifted(400, dz)]
    else:
        targets += [shifted(400, dz), shifted(-400, dz)]

old = RDK.Item('Paint_Side2', robolink.ITEM_TYPE_PROGRAM)
if old.Valid():
    old.Delete()

prog = RDK.AddProgram('Paint_Side2', robot)
prog.setPoseFrame(frame)
prog.setPoseTool(tool)

prog.MoveJ(targets[0])
for t in targets[1:]:
    prog.MoveL(t)

print("Done: Paint_Side2 created with", len(targets), "targets")