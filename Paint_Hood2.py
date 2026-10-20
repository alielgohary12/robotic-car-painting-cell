from robodk import robolink, robomath as rm

RDK = robolink.Robolink()
robot = RDK.Item('ABB IRB 6700-235/2.65', robolink.ITEM_TYPE_ROBOT)
frame = RDK.Item('Car_Frame', robolink.ITEM_TYPE_FRAME)
tool  = RDK.Item('Generic Paint Sprayer', robolink.ITEM_TYPE_TOOL)

robot.setPoseFrame(frame)
robot.setPoseTool(tool)

NAME  = 'Paint_Hood2'
SPAN  = 100
STEP  = 60
LINES = 3

base_pose = robot.Pose()
print("Start pose:", base_pose)

targets = []
for i in range(LINES):
    dy = (i - (LINES - 1) / 2.0) * STEP
    xs = (-SPAN, SPAN) if i % 2 == 0 else (SPAN, -SPAN)
    for x in xs:
        targets.append(rm.transl(x, dy, 0) * base_pose)

# Safe point: 300 mm above the hood
safe = rm.transl(-300, 0, 500) * targets[0]

old = RDK.Item(NAME, robolink.ITEM_TYPE_PROGRAM)
if old.Valid():
    old.Delete()

prog = RDK.AddProgram(NAME, robot)
prog.setPoseFrame(frame)
prog.setPoseTool(tool)

prog.MoveJ(safe)
for t in targets:
    prog.MoveJ(t)
prog.MoveJ(safe)

print("Created", NAME)