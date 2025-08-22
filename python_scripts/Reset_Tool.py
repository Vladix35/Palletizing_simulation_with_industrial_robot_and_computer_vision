# Type help("robolink") or help("robodk") for more information
# Press F5 to run the script
# Documentation: https://robodk.com/doc/en/RoboDK-API.html
# Reference:     https://robodk.com/doc/en/PythonAPI/index.html
# Note: It is not required to keep a copy of this file, your python script is saved with the station
from robodk import robolink
RDK = robolink.Robolink()

#----- CONSTANT -----

TOOL_NAME1 = 'OnRobot VGC10 Vacuum Gripper' #Name of the ref object to copy

#----- PROGRAM -----
tool1 = RDK.Item(TOOL_NAME1,robolink.ITEM_TYPE_TOOL)


if tool1.Valid():
    for item in tool1.Childs():
        if item.Type() == robolink.ITEM_TYPE_OBJECT:
            item.Delete()



