from robodk.robolink import *  # RoboDK API
from robodk.robomath import *  # Robot toolbox

RDK = Robolink()

PlaceTargetSmallBoxes  = RDK.Item('PlaceTargetSmallBoxes')     # Получение объекта target по имени

position_array = PlaceTargetSmallBoxes.Pose().Pos()             # the same can be applied to targets (taught position)

x_max = 450.000
y_max = -300.000


if position_array[1] < y_max:
    position_array[1] += 300
    PlaceTargetSmallBoxes.setPose(Pose(position_array[0], position_array[1], position_array[2], -180.000, -0.000, 180.000))  # Установите обновленные значения позиции target

elif position_array[0] < x_max:
    position_array[0] += 250
    position_array[1] = -1130.000
    PlaceTargetSmallBoxes.setPose(Pose(position_array[0], position_array[1], position_array[2], -180.000, -0.000, 180.000))  # Установите обновленные значения позиции target

else:
    position_array[0] = -18.297
    position_array[1] = -1130.000
    position_array[2] += 108.341
    PlaceTargetSmallBoxes.setPose(Pose(position_array[0], position_array[1], position_array[2], -180.000, -0.000, 180.000))  # Установите обновленные значения позиции target

# #PlaceTargetSmallBoxes.setPose(Pose(-18.297, -1130.000, -221.659,  -180.000, -0.000, 180.000))