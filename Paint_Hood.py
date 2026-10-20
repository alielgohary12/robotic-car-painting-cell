from robodk import robolink, robomath as rm

RDK = robolink.Robolink()
robot = RDK.Item('ABB IRB 6700-235/2.65', robolink.ITEM_TYPE_ROBOT)
frame = RDK.Item('Car_Frame', robolink.ITEM_TYPE_FRAME)
tool  = RDK.Item('Generic Paint Sprayer', robolink.ITEM_TYPE_TOOL)

robot.setPoseFrame(frame)
robot.setPoseTool(tool)

# ---- Hood settings ----
NAME  = 'Paint_Hood'
SPAN  = 150     # half-length of raster along X (mm)
STEP  = 80     # spacing between raster lines (mm)
LINES = 3       # number of raster lines
# -----------------------

base_pose = robot.Pose()   # robot must already stand on a reachable hood point
print("Start pose:", base_pose)

targets = []
for i in range(LINES):
    dy = (i - (LINES - 1) / 2.0) * STEP
    xs = (-SPAN, SPAN) if i % 2 == 0 else (SPAN, -SPAN)
    for x in xs:
        targets.append(rm.transl(x, dy, 0) * base_pose)

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