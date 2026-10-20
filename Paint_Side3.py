from robodk import robolink, robomath as rm

RDK = robolink.Robolink()
robot = RDK.Item('ABB IRB 6700-235/2.65', robolink.ITEM_TYPE_ROBOT)
frame = RDK.Item('Car_Frame', robolink.ITEM_TYPE_FRAME)
tool  = RDK.Item('Generic Paint Sprayer', robolink.ITEM_TYPE_TOOL)

print("valid:", robot.Valid(), frame.Valid(), tool.Valid())

robot.setPoseFrame(frame)
robot.setPoseTool(tool)

# Current gun pose in Car_Frame (a pose the robot reached by jogging)
base_pose = robot.Pose()
print("Start pose:", base_pose)

def shifted(dx, dz):
    # same orientation, shifted along Car_Frame X and Z
    return rm.transl(dx, 0, dz) * base_pose

# Small raster: 3 lines, +-300 mm along the car length
targets = []
for i, dz in enumerate([-100, 0, 100]):
    if i % 2 == 0:
        targets += [shifted(-300, dz), shifted(300, dz)]
    else:
        targets += [shifted(300, dz), shifted(-300, dz)]

# Remove old program if it exists
old = RDK.Item('Paint_Side3', robolink.ITEM_TYPE_PROGRAM)
if old.Valid():
    old.Delete()

prog = RDK.AddProgram('Paint_Side3', robot)
prog.setPoseFrame(frame)
prog.setPoseTool(tool)

prog.MoveJ(targets[0])
for t in targets[1:]:
    prog.MoveL(t)

print("Done: Paint_Side3 created with", len(targets), "targets")