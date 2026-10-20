from robodk import robolink, robomath as rm

RDK = robolink.Robolink()
car = RDK.Item('Car_Body', robolink.ITEM_TYPE_OBJECT)

# Measured bounding box (in Car_Frame coordinates, before rotation)
minx, miny, minz = 268.8, 38.6, 201.4
maxx, maxy, maxz = 2250.3, 4838.1, 1551.0

cx = (minx + maxx) / 2      # width center
cy = (miny + maxy) / 2      # length center
GROUND_CLEARANCE = 150      # mm, underside above floor

# Step 1: move the car so its bbox center is at the frame origin
# and its underside is at Z = GROUND_CLEARANCE
# Step 2: rotate 90 deg about Z so length lies along X
pose = rm.rotz(rm.pi/2) * rm.transl(-cx, -cy, GROUND_CLEARANCE - minz)

car.setPose(pose)
print("Car placed. Pose:\n", pose)