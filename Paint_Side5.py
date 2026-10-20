from robodk import robolink, robomath as rm

RDK = robolink.Robolink()
robot = RDK.Item('ABB IRB 6700-235/2.65', robolink.ITEM_TYPE_ROBOT)
frame = RDK.Item('Car_Frame', robolink.ITEM_TYPE_FRAME)
tool  = RDK.Item('Generic Paint Sprayer', robolink.ITEM_TYPE_TOOL)

robot.setPoseFrame(frame)
robot.setPoseTool(tool)

NAME = 'Paint_Side5'
base_pose = robot.Pose() * rm.rotx(rm.pi/12)   # tilt 15 degrees
print("Start pose:", base_pose)

def shifted(dx, dz):
    return rm.transl(dx, 0, dz) * base_pose

targets = []
for i, dz in enumerate([-100, 0, 100]):
    xs = (-300, 300) if i % 2 == 0 else (300, -300)
    for x in xs:
        targets.append(shifted(x, dz))

# Safe approach: same point, pulled back 400 mm away from the car (-Y)
safe = rm.transl(0, -150, 100) * targets[0]

old = RDK.Item(NAME, robolink.ITEM_TYPE_PROGRAM)
if old.Valid():
    old.Delete()

prog = RDK.AddProgram(NAME, robot)
prog.setPoseFrame(frame)
prog.setPoseTool(tool)

prog.MoveJ(safe)
prog.MoveJ(targets[0])
for t in targets[1:]:
    prog.MoveJ(t)
prog.MoveJ(safe)

print("Created", NAME)