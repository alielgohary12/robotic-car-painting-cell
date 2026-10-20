from robodk import robolink, robomath

RDK = robolink.Robolink()
car = RDK.Item('Car_Body', robolink.ITEM_TYPE_OBJECT)

car.Scale(2.655)
print("Scaled. Now re-export and re-measure to confirm.")