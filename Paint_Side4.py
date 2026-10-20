from robodk import robolink, robomath as rm

RDK = robolink.Robolink()
robot = RDK.Item('ABB IRB 6700-235/2.65', robolink.ITEM_TYPE_ROBOT)
frame = RDK.Item('Car_Frame', robolink.ITEM_TYPE_FRAME)
tool  = RDK.Item('Generic Paint Sprayer', robolink.ITEM_TYPE_TOOL)

robot.setPoseFrame(frame)
robot.setPoseTool(tool)

# Raster definition in Car_Frame (mm). Car side surface is at Y = -990.
Y_GUN = -1200
X_LIST = (-300, 300)
Z_LIST = (500, 650, 800)

# Candidate gun orientations (tool Z pointing toward the car, +Y)
candidates = {
    'rotx(-90)': rm.rotx(-rm.pi/2),
    'rotx(+90)': rm.rotx(rm.pi/2),
    'rotx(-90) roty(+30)': rm.rotx(-rm.pi/2) * rm.roty(rm.pi/6),
    'rotx(-90) roty(-30)': rm.rotx(-rm.pi/2) * rm.roty(-rm.pi/6),
}

def build_targets(orient):
    t = []
    for i, z in enumerate(Z_LIST):
        xs = X_LIST if i % 2 == 0 else X_LIST[::-1]
        for x in xs:
            t.append(rm.transl(x, Y_GUN, z) * orient)
    return t

def all_reachable(targets):
    for p in targets:
        if not robot.SolveIK_All(p, tool=None) if False else False:
            pass
    # use SolveIK on each target (returns joints, empty if unreachable)
    for p in targets:
        j = robot.SolveIK(p)
        if j is None or len(j.list()) < 6:
            return False
    return True

best = None
for name, orient in candidates.items():
    targets = build_targets(orient)
    ok = all_reachable(targets)
    print(name, '->', 'ALL REACHABLE' if ok else 'not reachable')
    if ok and best is None:
        best = (name, targets)

if best is None:
    print("No candidate orientation works. Send me this output.")
else:
    name, targets = best
    old = RDK.Item('Paint_Side4', robolink.ITEM_TYPE_PROGRAM)
    if old.Valid():
        old.Delete()
    prog = RDK.AddProgram('Paint_Side4', robot)
    prog.setPoseFrame(frame)
    prog.setPoseTool(tool)
    prog.MoveJ(targets[0])
    for p in targets[1:]:
        prog.MoveL(p)
    print("Created Paint_Side4 using", name)