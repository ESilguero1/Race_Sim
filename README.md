# YAY CARS GO VROOM
## Mostly realistic car physics
Cars drive with simulated velocity and heading using net forces of engine, friction and drag using realistic values of constants (mass, friction and drag coefficients, engine torque, wheelbase, and, of course, gravity).

Cars can collide with walls (but only from one specified direction, otherwise it glitches). They bounce off with a refelcted velocity with a slightly smaller magnitude depending on the wall elasticity coefficient.

Cars can also collide with each other, and "trade" velocity due to having equal masses. The resulting velocity is scaled based on the car elasticity coefficient.

When the car goes too fast and skids, marks are produced on the track.

## Editable Map
Walls can be dragged, rotated, and infinitely spawned. The map is also loaded on start and saved on exit, so you don't have to redo the map every time.

## Any number of players (kind of)
Cars can be spawned and bound to keys, until you run out of keyboard space.

## Distance sensors
Long and short range distance sensors can be attached to cars to allow for automated control! Raycasting is used to find distance, and that distance can be used in a control algorithm to drive automatically.

## Current progress:
https://github.com/user-attachments/assets/98777a23-4ac6-4352-bc96-ddf507532d60

## Working on:
Refining PID controller to create a versatile racer.
