---
title: Introduction and Connections
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

Introduction and Connections
============================
Use the first couple of days of class to get students ramped up with the system.  The goal of this section is to get students familiar with the system and setup to have a ship successfully connect to the server and have it execute a command. 

<a name="objective"></a>Objective
---------------------------------
Make sure each student can successfully register a ship and appear on the server before continuing. 

<a name="config"></a>Suggested Configuration
--------------------------------
It is a useful first exercise for the teacher to understand a little bit about how Space Battle configuration works.  To do so, you can simply modify the machine_fullscreen.cfg file included with the server to add additional sections to increase the number of objects in the world:

    [Asteroid]
    number = 8
    
    [Planet]
    number = 3
    
    [BlackHole]
    number = 1
    
    [Nebula]
    number = 2

This helps create a greater visual impact when first introducing students to Space Battle.  This can then be used on the command-line:

    SBA_Serv machine_fullscreen.cfg
 
<a name="resources"></a>Resources
------------------------------

 * [Client Setup](../client/index.html)
  * [jGRASP](../client/jGRASP/index.html)
  * [Eclipse](../client/Eclipse/index.html)
 * [Server Setup](../server/setup.html)
 * [Server Configuration](../server/config.html)
 
<a name="classroom"></a>Classroom Notes
--------------------------------
First, get students to start the IDE and add the jars to their classpath (see Client Setup Instruction supplemental document for more info). 

Then introduce the BasicSpaceship abstract class and have students implement the registerShip method and the getNextCommand method (return an IdleCommand at first). 

After most students have connected, introduce the RotateCommand and start talking about the dynamics of how the system calls the ship responds with a command for the server to execute. 

<a name="commands"></a>Commands Used
--------------------------------
[IdleCommand](http://mikeware.github.io/SpaceBattleArena/client/java_doc/ihs/apcs/spacebattle/commands/IdleCommand.html), [RotateCommand](http://mikeware.github.io/SpaceBattleArena/client/java_doc/ihs/apcs/spacebattle/commands/RotateCommand.html)

<a name="api"></a>API Used
-----------------------------
[BasicSpaceship](http://mikeware.github.io/SpaceBattleArena/client/java_doc/ihs/apcs/spacebattle/BasicSpaceship.html), [TextClient](http://mikeware.github.io/SpaceBattleArena/client/java_doc/ihs/apcs/spacebattle/TextClient.html)
