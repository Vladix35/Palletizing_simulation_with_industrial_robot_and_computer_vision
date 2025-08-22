from robodk.robolink import *  # RoboDK API
from robodk.robomath import *  # Robot toolbox

RDK = Robolink()

PlaceTargetMediumBoxes  = RDK.Item('PlaceTargetMediumBoxes')     # Получение объекта target по имени
ApproachMediumBoxes  = RDK.Item('ApproachMediumBoxes')

position_array_p = PlaceTargetMediumBoxes.Pose().Pos()             # the same can be applied to targets (taught position)
position_array_a = ApproachMediumBoxes.Pose().Pos()

x_max = -250.000
y_max = -2000.000


if position_array_p[0] < x_max:
    position_array_p[0] += 300
    PlaceTargetMediumBoxes.setPose(Pose(position_array_p[0], position_array_p[1], position_array_p[2], 180.000, -0.000, -90.000))  # Установите обновленные значения позиции target

    position_array_a[0] += 300
    ApproachMediumBoxes.setPose(Pose(position_array_a[0], position_array_a[1], position_array_a[2], 180.000, -0.000, -90.000))
    
elif position_array_p[1] > y_max:
    position_array_p[0] = -1120.000
    position_array_p[1] -= 250
    PlaceTargetMediumBoxes.setPose(Pose(position_array_p[0], position_array_p[1], position_array_p[2], 180.000, -0.000, -90.000))  # Установите обновленные значения позиции target

    position_array_a[0] = -1120.000
    #position_array_a[1] -= 250
    ApproachMediumBoxes.setPose(Pose(position_array_a[0], position_array_a[1], position_array_a[2], 180.000, -0.000, -90.000))
    
else:
    position_array_p[0] = -1120.000
    position_array_p[1] = -1540.000
    position_array_p[2] += 162.512
    PlaceTargetMediumBoxes.setPose(Pose(position_array_p[0], position_array_p[1], position_array_p[2], 180.000, -0.000, -90.000))  # Установите обновленные значения позиции target

    position_array_a[0] = -1120.000
    #position_array_a[1] = -1540.000
    ApproachMediumBoxes.setPose(Pose(position_array_a[0], position_array_a[1], position_array_a[2], 180.000, -0.000, -90.000))
# #PlaceTargetMediumBoxes.setPose(Pose(-1120.000, -1540.000, -167.488,  180.000, -0.000, -90.000))
