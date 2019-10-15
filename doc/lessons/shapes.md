---
title: Shapes in Space
nav:
 - { url: "index.html", title: "Lessons" }
outline-header: Lessons
outline:
 - { url: "#objective", title: "Objectives" }
 - { url: "#config", title: "Suggested Configuration" }
 - { url: "#resources", title: "Resources" }
 - { url: "#classroom", title: "Classroom Notes" }
 - { url: "#commands", title: "Commands Used" }
 - { url: "#api", title: "API Used" }
---

Shapes in Space
===============
After students can move and stop their ship, it is time to introduce more complex movement patterns and the idea of repetition within the confines of the call/response pattern.

It turns out drawing turtle graphics in space is a lot harder than you would think.  Space Battle provides *'laser nodes'* which allow for the drawing of shapes in space.

This lesson works towards students getting more comfortable with maneuvering their ship by incrementally learning to draw different shapes such as rectangles, stars, spirals, and an octagon circumscribed around a square.

_This is a great callback lesson if you started off with turtle graphics at the start of the year.  However, we recommend skipping it if you did not do turtle graphics previously, unless you're short on time or want to end with the next lesson instead of moving towards a larger more complex competition.  We suggest this as we've found giving students more time to learn Radar earlier sets them up for greater success later._

<a name="objective"></a>Objectives
---------------------------------
Each student can write multiple ships which draw incrementally more complex shapes:

1. Rectangle
2. 5-pointed Star
3. Spiral
4. 'OctoSquare' - Octagon circumscribed around a square without the two shapes touching.

<a name="config"></a>Suggested Configuration
--------------------------------
A find the middle game configuration is provided in the server package:

    SBA_Serv machine_fullscreen.cfg empty.cfg no_collide.cfg no_advanced_commands.cfg
 
The provided configuration changes the game on the server to include no objects:

	[Nebula]
	number = 0

	[Planet]
	number = 0

	[BlackHole]
	number = 0

	[Asteroid]
	number = 0
	
As well as turns off collisions:

	[World]
	collisions = false
	
And disables all advanced commands:

	[Server]
	disable_commands = AllStopCommand,CloakCommand,FireTorpedoCommand,RaiseShieldsCommand,RepairCommand,WarpCommand
	
Extra specifics on the game configuration can be found on the game resource page.
 
<a name="resources"></a>Resources
------------------------------

None
 
<a name="classroom"></a>Classroom Notes
--------------------------------
A Space Battle ‘Laser Nodes’ is a non-tangible entity which will project laser lines in space.  They always work in pairs, thus dropping one Laser Node will not help create a stable shape until another one is dropped.  Once a pair has been dropped, they will perpetually display a 'laser' line of the ship’s color (as specified in registerShip) in space indefinitely.  A single 'odd' laser node will always project back to the ship which deployed it.

Using this new command, students can now draw shapes in space.  You should discuss and walk through drawing a square as an example using a counter to dispatch commands to draw a single side of the square and resetting it to draw the next 3 sides. 

Once they are able to have a ship perpetually draw a square, see if they can tell the ship to move away and rotate (or idle) after drawing the single shape.

Afterwards, on their own students should work on creating a 5-pointed star. 

For the next few days, as an in-class assignment, the students should also work on creating a Spiral (inwards or outwards, doesn’t have to be perfectly smooth\*) and an ‘OctoSquare’.  We define an ‘OctoSquare’ as an octagon circumscribed around a square.  However, the square should not touch the octagon. 

**\* Note:** Ambitious students can try using the new *SteerCommand* in order to create a smoother spiral.

<a name="commands"></a>Commands Used
--------------------------------
[IdleCommand](http://mikeware.github.io/SpaceBattleArena/client/java_doc/ihs/apcs/spacebattle/commands/IdleCommand.html), [RotateCommand](http://mikeware.github.io/SpaceBattleArena/client/java_doc/ihs/apcs/spacebattle/commands/RotateCommand.html)
[ThrustCommand](http://mikeware.github.io/SpaceBattleArena/client/java_doc/ihs/apcs/spacebattle/commands/ThrustCommand.html), [DeployLaserBeaconCommand](http://mikeware.github.io/SpaceBattleArena/client/java_doc/ihs/apcs/spacebattle/commands/DeployLaserBeaconCommand.html)

Advanced: [SteerCommand](http://mikeware.github.io/SpaceBattleArena/client/java_doc/ihs/apcs/spacebattle/commands/SteerCommand.html), [DestroyAllLaserBeaconCommand](http://mikeware.github.io/SpaceBattleArena/client/java_doc/ihs/apcs/spacebattle/commands/DestroyAllLaserBeaconsCommand.html)

<a name="api"></a>API Used
-----------------------------

None
