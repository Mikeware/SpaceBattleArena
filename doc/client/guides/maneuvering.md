---
title: Maneuvering in Space
nav:
 - { url: "index.html", title: "Space Battle Academy" }
---

Remember, where we're going there are no roads...
=========

Space is a vast environment which behaves differently than you experience most things here on earth.  It is best to keep this in mind as you instruct your Ship to move about its environment.

Firstly, Space has no friction.  This means that once you thrust for any period of time...

> You will continue to move in the opposite direction that you thrust 'FOREVER'. 
 
Basically, in order to stop you need to apply an equal amount of thrust in the *opposite* direction that you initially thrusted.  However,  if you thrust in complex combinations (especially after rotating) or if some other entity changes the direction of your travel, it can be difficult to determine exactly how to stop.

For your convenience there are a couple of commands provided which can help you slow or stop your spaceship, such as the [BrakeCommand](../java_doc/ihs/apcs/spacebattle/commands/BrakeCommand.html).

The other force in space which has a different effect on travel is gravity.  As you travel in your spaceship, you must remember that it will gravitate towards other celestial objects.  This means your **direction** of travel will be affected as you pass within sufficient range of these objects.

> Your ship's movement can also be affected by colliding with other objects like asteroids or other ships.

Your **orientation** will only change if you issue a [RotateCommand](../java_doc/ihs/apcs/spacebattle/commands/RotateCommand.html).

Navigating your environment, staying on target, and avoiding and recovering from obstacles will be key in your success on your future missions.
