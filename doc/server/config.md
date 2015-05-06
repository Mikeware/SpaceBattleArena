---
title: Server Configuration
nav:
 - { url: "index.html", title: "Server Information" }
outline-header: Outline
outline:
 - { url: "#overview", title: "Overview" }
 - { url: "#format", title: "Format" }
 - { url: "#screen", title: "[Screen]" }
 - { url: "#world", title: "[World]" }
 - { url: "#server", title: "[Server]" }
 - { url: "#asteroid", title: "[Asteroid]" }
 - { url: "#planet", title: "[Planet]" }
 - { url: "#blackhole", title: "[BlackHole]" }
 - { url: "#nebula", title: "[Nebula]" }
 - { url: "#game", title: "[Game]" }
---

Server Configuration
=============

<a name="overview"></a>Overview
-----------

Space Battle Arena is highly configurable.  SBA uses a standard type of configuration file format to set options for how the server should run and behave.  

SBA comes with a set of configuration files for different purposes.  However, you'll probably want to create your own configuration file to represent the settings of your machine and its display (see the [[Screen]](#screen) section below).

The **run** command mentioned in the server [setup](setup.html) page can take an optional second config file.  This can be handy to use one config to keep your standard options and a second one to use for any game or activity of the day.

In fact the configuration examples provided with the server do just that and setup a 'machine' file to specify the size of the window and then a 'lesson' file to use for the activity of the day in class.

	run machine_test.cfg lesson_findthemiddle.cfg


<a name="format"></a>Format
-----------

The configuration file is composed of a number of sections with each section containing one or more options.  It follows the format:

	[Section Name]
	option1name = value
	option2name = value
	
	[Section 2 Name]
	optionname = value
	
	etc...
	
The rest of this chapter will be comprised of headers for each of the *section* names and then sub-headers for each *option* (and its type) and then a paragraph listing its purpose and possible values.

Possible value types include integer, boolean, string, and percent:

 * Integers will be zero or positive only.
 * Booleans will either be **true** or **false**.
 * String values will be provided without quotation marks and possible values will be specified in the specific option listing.
 * Percent values are decimal values between 0.0 and 1.0.  These may be part of a set which is expected to total 1.0.

You may also see advanced constructs such as Tuples in parenthesis () or Lists in [], but if you are familiar with [JSON](http://json.org/) formatting, then it shouldn't be hard to follow.


<a name="screen"></a>[Screen]
---------------------------------------
This section contains options pertaining to the graphical window created to run the SBA server.  It will affect how SBA is presented to you.

###horz_res = integer
Specifies the horizontal resolution of the SBA window (in pixels).  This should match your monitor resolution if you plan to run the game in fullscreen.

###vert_res = integer
Specifies the vertical resolution of the SBA window (in pixels).  This should match your monitor resolution if you plan to run the game in fullscreen.

###fullscreen = boolean
Specifies whether or not SBA should run fullscreen or in a window.

###showstats = boolean
If this option is enabled, the server will start with some basic GUI options already enabled showing statistics about a player’s ship


<a name="world"></a>[World]
---------------------------------------
This section contains options for how large the universe is.  These options should be set to be *at least* as large as the Screen options, but can be larger.  *It is generally recommended that they are each 1.5 or 2 times the value of their corresponding Screen values.*

###width = integer
Horizontal length of the universe in pixels.

###height = integer
Vertical length of the universe in pixels.


<a name="server"></a>[Server]
---------------------------------------
This section of options controls how the server should behave and accept connections from clients.

###multipleconnections = boolean
This option when enabled allows the same client machine to be connected to the server more than once.  Otherwise, each IP address is only allowed to connect a single time to a server instance.  This can cause issues if a client’s connection unexpectedly terminates.

###port = integer
The TCP/IP port that the server should run on.  If this is changed from the default (**2012**), then a third parameter of a port number must be passed in when running the TextClient class from a Java client.

###maximages = integer
This specifies the number of images that can be used for ships in the *GUI\Graphics\Ships* directory.  Use an existing ship image as a template to create more ship images.  Each frame of a ship should be contained in a 64x64 pixel square within the image.  The top row of images show a normal ship, the bottom a cloaked ship.  The first image is neutral, then left thruster firing, front thrusters, right thruster, back thruster, all thrusters (braking), and warping.


<a name="asteroid"></a>[Asteroid]
---------------------------------------
Asteroids are flying debris in space.  They start off with a set amount of momentum and will continue flying in space until impacting ships or destroyed by torpedos.

###number = integer
The number of asteroids to generate in the universe.


<a name="planet"></a>[Planet]
---------------------------------------
Planets have gravity wells which can pull ships towards them.  They are solid and will cause damage to ships that impact them.

###number = integer
The number of planets to generate in the universe.

###range_min = integer
see range_max

###range_max = integer
These two range values correspond to the distance away from a planet's center that its gravity field should pull ships in.  A random value will be generated between the **range_min** and **range_max** values.  These are typically **112** and **192**.

###pull_min = integer
see pull_max

###pull_max = integer
These two values correspond to the amount of pull the gravity will have on ships.  Larger values mean ships will get pulled in quicker and will have a harder time escaping.  A random value will be generated between **pull_min** and **pull_max**.  These are typically **8** and **24**.


<a name="blackhole"></a>[BlackHole]
---------------------------------------
Black Holes have stronger gravity wells than planets, but can be passed through their center.  They are harder to escape from.

They have the exact same configuration values as [Planets](#planet).  However, the default range values are **64** and **208**.  The default pull values are **52** and **72**.


<a name="nebula"></a>[Nebula]
---------------------------------------
Nebulas are a celestial body which impart a drag effect on ships causing them to slow down or eventually stop if they are not thrusting.

###number = integer
The number of Nebulas to generate in the universe.

###sizes = list of tuples
This is a list of the available sizes of nebulas.  The tuple pair is the total length of the **major** and **minor** axes of an ellipse.  There also needs to be a corresponding image in the *GUI\Graphics\Nebula* folder with the name **NebulaMAJORxMINOR** where 'MAJOR' and 'MINOR' are replaced with the values of the size of the Nebula.  These values should be placed in a list.  E.g.

	sizes=[(512,128),(384,256)]

###pull_min = integer
see pull_max

###pull_max = integer
These two values correspond to the amount of pull the drag will have on ships.  Larger values mean ships will slow down faster.  It'd best not to make these values higher than the Ship's Thruster force of 3500.  A random value will be generated between **pull_min** and **pull_max**.  These are typically **1750** and **2500**.


<a name="game"></a>[Game]
---------------------------------------
Main options for the behavior of the simulation and which tournament rules should be applied.

###sound = boolean
Determines if sounds should be played or not.

###autostart = boolean
When set to true the game/round will automatically start when the server is run.  Otherwise, it will wait for you to press the space key.

###allowafterstart = boolean
Can players join the server after the game has already started?

###allowreentry = boolean
Can a player join the server again if they had connected previously and disconnected?

###collisions = boolean
Turn collision detection on/off in the physics engine.  Useful for introductions to the world without worrying about actual interference.

###disconnectplayersafterround = boolean
Should clients be disconnected from the server after they have completed a round?

###radarname = boolean
Determines if the name of the ship can be obtained through a Radar Command or not.

###tournament = boolean
Should the game be run in a tournament setting where connected players are split into a number of groups.  Each winner of the game in a group proceeds to a final bracket to determine a winner.  Each round will automatically be paired, timed, and calculated.  Just hit space to start each round.

###tournamentgroups = integer
How many groups should the number of clients connected be broken into for the tournament?  E.g. Setting this value to 5 and having 30 clients connected would result in 5 rounds of 6 players each and a final round with the winners of each group.  Raising this number to higher values requires more vertical real-estate for the tournament display board.

###roundtime = integer
How long each game round should last in seconds.

###resetworldeachround = boolean
Should the world be cleared of all objects and recreated between each round of play?

###rungame = string
Name of the game to be played on the server.  See more info in the Competitions section about running games.

To just have a standard universe running, use **BasicGame**.
