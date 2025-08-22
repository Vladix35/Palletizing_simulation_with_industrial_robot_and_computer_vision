# Type help("robolink") or help("robodk") for more information
# Press F5 to run the script
# Documentation: https://robodk.com/doc/en/RoboDK-API.html
# Reference:     https://robodk.com/doc/en/PythonAPI/index.html
# Note: It is not required to keep a copy of this file, your python script is saved with the station
from robodk import robolink
RDK = robolink.Robolink()

#This program reinitialize every mechanisms in the list to position 0

REFERENCE_FRAME = "Box_Conveyor_Ref"
COLLISION_CUBE_NAME = "Collision Cube"

#------- Program ------
frame = RDK.Item(REFERENCE_FRAME, robolink.ITEM_TYPE_FRAME)
Collision_Cube = RDK.Item(COLLISION_CUBE_NAME, robolink.ITEM_TYPE_OBJECT)


if frame.Valid():
    for item in frame.Childs():
        if item.Collision(Collision_Cube) or item.IsInside(Collision_Cube):
            if item.Type() == robolink.ITEM_TYPE_OBJECT:
                item.Delete()

