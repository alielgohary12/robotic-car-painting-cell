from robodk import robolink, robomath as rm

RDK = robolink.Robolink()
robot = RDK.Item('ABB IRB 6700-235/2.65', robolink.ITEM_TYPE_ROBOT)
frame = RDK.Item('Car_Frame', robolink.ITEM_TYPE_FRAME)
tool  = RDK.Item('Generic Paint Sprayer', robolink.ITEM_TYPE_TOOL)

robot.setPoseFrame(frame)
robot.setPoseTool(tool)

# Raster parameters (in Car_Frame, mm)
X_MIN, X_MAX = -1200, 1200      # along the car length (reachable part)
Z_MIN, Z_MAX = 500, 1200        # height range of the side panel
Y_STAND = -1150                 # gun position (car side surface ~ -990)
STEP_Z = 150                    # raster line spacing

# Tool Z axis must point toward the car (+Y in Car_Frame)
# Rotation: tool Z -> +Y  (rotate about X by -90 deg)
orient = rm.rotx(-rm.pi/2)

prog = RDK.Item('Paint_Side', robolink.ITEM_TYPE_PROGRAM)
if prog.Valid():
    prog.Delete()
prog = RDK.AddProgram('Paint_Side', robot)
prog.setPoseFrame(frame)
prog.setPoseTool(tool)

# Safe approach
approach = rm.transl(X_MIN, Y_STAND - 400, Z_MAX + 200) * orient
prog.MoveJ(approach)

z = Z_MIN
direction = 1
failed = 0
while z <= Z_MAX:
    xs = (X_MIN, X_MAX) if direction == 1 else (X_MAX, X_MIN)
    p1 = rm.transl(xs[0], Y_STAND, z) * orient
    p2 = rm.transl(xs[1], Y_STAND, z) * orient
    prog.MoveL(p1)
    prog.MoveL(p2)
    z += STEP_Z
    direction *= -1

prog.MoveJ(approach)
print("Program 'Paint_Side' created. Run it from the station tree.")