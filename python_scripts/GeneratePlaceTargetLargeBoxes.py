from robodk.robolink import *  # RoboDK API
from robodk.robomath import *  # Robot toolbox

RDK = Robolink()

PlaceTargetLargeBoxes  = RDK.Item('PlaceTargetLargeBoxes')     # Получение объекта target по имени

position_array = PlaceTargetLargeBoxes.Pose().Pos()             # the same can be applied to targets (taught position)

x_max = -1300.000
y_max = -350.000


if position_array[1] < y_max:
    position_array[1] += 400
    PlaceTargetLargeBoxes.setPose(Pose(position_array[0], position_array[1], position_array[2],  180.000, 0.000, 0.000))  # Установите обновленные значения позиции target

elif position_array[0] < x_max:
    position_array[0] += 275
    position_array[1] = -1130.000
    PlaceTargetLargeBoxes.setPose(Pose(position_array[0], position_array[1], position_array[2],  180.000, 0.000, 0.000))  # Установите обновленные значения позиции target

else:
    position_array[0] = -1840.000
    position_array[1] = -1130.000
    position_array[2] += 216.683
    PlaceTargetLargeBoxes.setPose(Pose(position_array[0], position_array[1], position_array[2],  180.000, 0.000, 0.000))  # Установите обновленные значения позиции target

# #PlaceTargetLargeBoxes.setPose(Pose(-1840.000, -1130.000, -113.317,  0.000, 0.000, 180.000))
[ -1840.000000, -1130.000000,  -113.317000,     0.000000,     0.000000,   180.000000 ]
