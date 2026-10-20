from robodk import robolink, robomath as rm
import sys

RDK = robolink.Robolink()
robot = RDK.Item('ABB IRB 6700-235/2.65', robolink.ITEM_TYPE_ROBOT)
frame = RDK.Item('Car_Frame', robolink.ITEM_TYPE_FRAME)
tool  = RDK.Item('Generic Paint Sprayer', robolink.ITEM_TYPE_TOOL)

robot.setPoseFrame(frame)
robot.setPoseTool(tool)

# ---- Edit only this block per surface ----
NAME = 'Paint_Roof'
SPAN = 600          # half-length of raster along X (mm)
STEP = 100          # spacing between raster lines (mm)
LINES = 5           # number of raster lines
AXIS = 'z'          # which axis the lines are stacked along: 'z' (side) or 'y' (roof/hood)
# ------------------------------------------

base_pose = robot.Pose()   # robot must be standing on a reachable start point
print("Start pose:", base_pose)

def shifted(dx, dline):
    if AXIS == 'z':
        return rm.transl(dx, 0, dline) * base_pose
    return rm.transl(dx, dline, 0) * base_pose

offsets = [(i - (LINES - 1) / 2.0) * STEP for i in range(LINES)]
targets = []
for i, d in enumerate(offsets):
    xs = (-SPAN, SPAN) if i % 2 == 0 else (SPAN, -SPAN)
    for x in xs:
        targets.append(shifted(x, d))

old = RDK.Item(NAME, robolink.ITEM_TYPE_PROGRAM)
if old.Valid():
    old.Delete()

prog = RDK.AddProgram(NAME, robot)
prog.setPoseFrame(frame)
prog.setPoseTool(tool)
prog.MoveJ(targets[0])
for t in targets[1:]:
    prog.MoveL(t)

print("Created", NAME, "with", len(targets), "targets")