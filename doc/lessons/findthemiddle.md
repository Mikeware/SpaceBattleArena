---
title: Find The Middle
nav:
 - { url: "index.html", title: "Lessons" }
outline-header: Lessons
outline:
 - { url: "#objective", title: "Objective" }
 - { url: "#config", title: "Suggested Configuration" }
 - { url: "#resources", title: "Resources" }
 - { url: "#classroom", title: "Classroom Notes" }
 - { url: "#commands", title: "Commands Used" }
 - { url: "#api", title: "API Used" }
---

Find The Middle
===============
After students are able to connect to the server, it is time to introduce a couple of new commands and an objective. This activity provides a suitable first challenge for students to get comfortable with the environment and thinking to program in this call and response fashion. 

<a name="objective"></a>Objective
---------------------------------
Each student can write a ship which finds the center of the universe, navigates to it, and can stay there.

<a name="config"></a>Suggested Configuration
--------------------------------
A find the middle game configuration is provided in the server package:

    SBA_Serv machine_fullscreen.cfg basicgame_findthemiddle.cfg
 
The provided configuration changes the game on the server:

	[Game]
	game = FindTheMiddle
	
As well as turns off collisions:

	[World]
	collisions = false
	
And disables a couple of commands:

	[Server]
	disable_commands = WarpCommand,FireTorpedoCommand,AllStopCommand
	
Extra specifics on the game configuration can be found on the game resource page.
 
<a name="resources"></a>Resouces
------------------------------

 * [Find The Middle](../games/findthemiddle.html)
 
<a name="classroom"></a>Classroom Notes
--------------------------------
Now that students are able to connect, the day should be spent going over commands (Rotate, Thrust, and Brake) and controlling a ship in space.  This is also a good point to talk about blocking (Rotate, Brake) vs. non-blocking commands (Thrust). 

Normally, when a command is given to the server, it *blocks* and waits for the command to finish before returning to ask for another command.  For instance, if you say IdleCommand(5.0), the command will execute for 5 seconds and then return.

However, when Thrust is given as a command, the server immediately returns and asks for a new command while your ship continues to thrust. This is the non-blocking paradigm.

Another notes about Thrust to go over are how the directions for thrust will move you in the opposite direction, as the parameter is the thruster's location to fire.  Also, thrust is a limited resource, so issuing multiple thrust commands at full power in succession will not result in anything outside a waste of energy.

The students objective is to get their ship from their spawning point to somewhere near the middle of the world.  They can use the parameters given to the registerShip method to calculate the mid-point of the universe.  Aim for students to have accomplished this by the end of the next day. 

The Point class also provides helpful methods to determine how to rotate a ship towards the center of the universe.

	ObjectStatus ship = env.getShipStatus();
	return new RotateCommand(ship.getPosition().getAngleTo(this.midpoint) - ship.getOrientation());

<a name="commands"></a>Commands Used
--------------------------------
[IdleCommand](http://mikeware.github.io/SpaceBattleArena/client/java_doc/ihs/apcs/spacebattle/commands/IdleCommand.html), [RotateCommand](http://mikeware.github.io/SpaceBattleArena/client/java_doc/ihs/apcs/spacebattle/commands/RotateCommand.html)
[ThrustCommand](http://mikeware.github.io/SpaceBattleArena/client/java_doc/ihs/apcs/spacebattle/commands/ThrustCommand.html)

<a name="api"></a>API Used
-----------------------------
[registerShip](http://mikeware.github.io/SpaceBattleArena/client/java_doc/ihs/apcs/spacebattle/BasicSpaceship.html#registerShip(int,%20int,%20int)), [Point](http://mikeware.github.io/SpaceBattleArena/client/java_doc/ihs/apcs/spacebattle/Point.html)
