# YAY CARS GO VROOM
## Mostly realistic car physics
Cars drive with simulated velocity and heading using net forces of engine, friction and drag using realistic values of constants (mass, friction and drag coefficients, engine torque, wheelbase, and, of course, gravity).

Cars can collide with walls (but only from one specified direction, otherwise it glitches). They bounce off with a refelcted velocity with a slightly smaller magnitude depending on the wall elasticity coefficient.

Cars can also collide with each other, and "trade" velocity due to having equal masses. The resulting velocity is scaled based on the car elasticity coefficient.

## Editable Map
Walls can be dragged, rotated, and infinitely spawned. The map is also loaded on start and saved on exit, so you don't have to redo the map every time.

## Any number of playser (kind of)
Cars can be spawned and bound to keys, until you run out of keyboard space.

## Working on:
Simulating distance sensors to allow for the implementation of automated cars!!