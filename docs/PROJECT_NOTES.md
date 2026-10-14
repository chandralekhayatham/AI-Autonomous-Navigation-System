# Project Notes

## Goal
Demonstrate autonomous navigation in a virtual 2D grid without physical robot hardware.

## Current implementation
- Deterministic grid-based obstacle map.
- A* path planning with Manhattan-distance heuristic and four-direction movement.
- Pygame animation of a virtual robot following the computed route.
- Keyboard controls to pause, reset, and add an obstacle that triggers replanning.

## Scope and limitations
This first version simulates obstacle locations as blocked grid cells. It does not use a camera, trained object detector, ROS, or physical sensors. It is an educational simulation, not a controller for real vehicles.
