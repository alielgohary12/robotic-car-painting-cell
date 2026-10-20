from robodk import robolink

RDK = robolink.Robolink()
robot = RDK.Item('ABB IRB 6700-235/2.65', robolink.ITEM_TYPE_ROBOT)

names = ['Paint_Side5', 'Paint_Roof2']

old = RDK.Item('Main_Program', robolink.ITEM_TYPE_PROGRAM)
if old.Valid():
    old.Delete()

home_joints = robot.JointsHome()

main = RDK.AddProgram('Main_Program', robot)
main.MoveJ(home_joints)
for n in names:
    p = RDK.Item(n, robolink.ITEM_TYPE_PROGRAM)
    if p.Valid():
        main.RunInstruction(n, robolink.INSTRUCTION_CALL_PROGRAM)
        main.MoveJ(home_joints)
        print("Added", n)
    else:
        print("MISSING:", n)