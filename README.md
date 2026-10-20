# Robotic Car Painting Cell Simulation

Name: Ali Mohamed Elgohary

Software used: RoboDK 6.1.1 (Free / Limited)

Robot selected: ABB IRB 6700-235/2.65

## Description
Simulation of an industrial robot painting a car body (4800 x 1981 x 1350 mm).

Raster paths are generated with the RoboDK Python API. Collision checking is

done with the RoboDK Collision Map.

## Results
- Near side panel: painted without collision (Paint_Side5)
- 
- Roof: painted without collision (Paint_Roof2)
- 
- Hood / trunk / front / rear / far side: outside the reach from a fixed
- 
  position. Proposed solution: linear track or turntable.

## Files
- Car_Painting_Cell_*.rdk : RoboDK station
- 
- *.py : Python scripts (cell setup, car placement, path generation)
- 
- car_final.stl : scaled and centered car model
- 
- Technical_Report.pdf : full report
