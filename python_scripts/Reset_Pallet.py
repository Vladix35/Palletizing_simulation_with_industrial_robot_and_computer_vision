# Type help("robolink") or help("robodk") for more information
# Press F5 to run the script
# Documentation: https://robodk.com/doc/en/RoboDK-API.html
# Reference:     https://robodk.com/doc/en/PythonAPI/index.html
# Note: It is not required to keep a copy of this file, your python script is saved with the station

# You can also use the new version of the API:
from robodk import robolink   # RoboDK API
from robodk import robomath    # Robot toolbox
RDK = robolink.Robolink()

#----- CONSTANT -----

FRAME = 'Pallet' #Name of the ref object to copy
PALLET = "Pallet 1200x800mm (Transverse)"

#----- PROGRAM -----
frame = RDK.Item(FRAME,robolink.ITEM_TYPE_FRAME)


if frame.Valid():
    for item in frame.Childs():
        if item.Type() == robolink.ITEM_TYPE_OBJECT:
            if item.Name() != PALLET:
                item.Delete()


RDK.setParam("RowBoxX",0)
RDK.setParam("RowBoxY",0)
RDK.setParam("RowBoxX_Buffer",0)