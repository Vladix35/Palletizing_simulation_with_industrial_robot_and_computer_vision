import random
from robodk import robolink, robomath

RDK = robolink.Robolink()
    
#----- Constants -----
REFERENCE_FRAME = 'Box_Conveyor_Ref'  # Name of the frame the object will move to
REFERENCE_FRAME_REF = 'Box_Init_Ref'
MECHANISM_NAME = "Vision_Conveyor"

PART_TRAVEL_MM = RDK.getParam("Conveyor_Travel")  # Travel for each box
NEW_REF_OBJECT_NAME = 'BoxRef'  # Name of the ref object to copy
NEW_OBJECT_NAME = 'Box'  # Name of the new object created

# List of predefined sizes for the boxes
BOX_SIZES = [0.5, 0.75, 1.0]

#------- Program ------
frame = RDK.Item(REFERENCE_FRAME, robolink.ITEM_TYPE_FRAME)
frame_ref = RDK.Item(REFERENCE_FRAME_REF, robolink.ITEM_TYPE_FRAME)
ref_obj = RDK.Item(NEW_REF_OBJECT_NAME, robolink.ITEM_TYPE_OBJECT)
mechanism = RDK.Item(MECHANISM_NAME, itemtype=robolink.ITEM_TYPE_ROBOT)

r = random.SystemRandom()

# Randomly choose one of the predefined box sizes
size = r.choice(BOX_SIZES)

x = r.uniform(0, 20)
y = r.uniform(-280, 280)
rotz = r.uniform(-80, 80)

copybox = r.uniform(0, 1)

RDK.setSimulationSpeed(3.5)

if frame.Valid() and ref_obj.Valid() and copybox > 0.1:

    ref_obj.Copy()
    new_obj = RDK.Paste()
    new_obj.setVisible(False)

    boxnum = RDK.getParam("Box_Num")
  
    RDK.setParam("Box_Num", boxnum + 1)

    new_obj.setName(NEW_OBJECT_NAME + " " + str(int(RDK.getParam("Box_Num"))))
    new_obj.setParent(frame_ref)

    new_obj.setPose(robomath.Offset(new_obj.Pose(), x, y, (frame_ref.Pose()[2, 3] * size) - frame_ref.Pose()[2, 3], 0, 0, rotz))
    new_obj.Scale(size)

    new_obj.setParentStatic(frame)
    new_obj.setVisible(True)
    RDK.Update()

if mechanism.Valid():
    mechanism.MoveJ(mechanism.Joints() + PART_TRAVEL_MM)
