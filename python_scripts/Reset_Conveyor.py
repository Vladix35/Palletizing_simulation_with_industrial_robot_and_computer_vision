# Type help("robolink") or help("robodk") for more information
# Press F5 to run the script
# Documentation: https://robodk.com/doc/en/RoboDK-API.html
# Reference:     https://robodk.com/doc/en/PythonAPI/index.html
# Note: It is not required to keep a copy of this file, your python script is saved with the station
from robodk import robolink
RDK = robolink.Robolink()

#This program reinitialize every mechanisms in the list to position 0
MECHANISM_NAME = "Vision_Conveyor"
REFERENCE_FRAME = "Box_Conveyor_Ref"
#------- Program ------
frame = RDK.Item(REFERENCE_FRAME, robolink.ITEM_TYPE_FRAME)


mechanism = RDK.Item(MECHANISM_NAME,itemtype=robolink.ITEM_TYPE_ROBOT)
if mechanism.Valid():
    mechanism.setJoints([0])


if frame.Valid():
    for item in frame.Childs():
        if item.Type() == robolink.ITEM_TYPE_OBJECT:
            item.Delete()

RDK.setParam("Box_Num", 0)
RDK.setParam("Box_Name", "")
RDK.setParam("Box_X", "")
RDK.setParam("Box_Y", "")
RDK.setParam("Box_Z", "")

RDK.setParam("Box_A", "")
RDK.setParam("Box_B", "")
RDK.setParam("Box_C", "")
RDK.setParam("Box_Name", "")
RDK.setParam("Box_Dect", "No")

