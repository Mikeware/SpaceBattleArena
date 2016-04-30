---
title: Server Configuration
nav:
 - { url: "index.html", title: "Server Information" }
outline-header: Outline
outline:
 - { url: "#overview", title: "Overview" }
 - { url: "#format", title: "Format" }
 - { url: "#application", title: "[Application]" }
 - { url: "#world", title: "[World]" }
 - { url: "#server", title: "[Server]" }
 - { url: "#spawnmanager", title: "Spawn Manager" }
 - { url: "#asteroid", title: "[Asteroid]" }
 - { url: "#dragon", title: "[Dragon]" }
 - { url: "#planet", title: "[Planet]" }
 - { url: "#blackhole", title: "[BlackHole]" }
 - { url: "#star", title: "[Star]" }
 - { url: "#nebula", title: "[Nebula]" }
 - { url: "#wormhole", title: "[WormHole]" }
 - { url: "#game", title: "[Game]" }
 - { url: "#tournament", title: "[Tournament]" }
---

Server Configuration
=============

<a name="overview"></a>Overview
-----------

Space Battle Arena is highly configurable.  SBA uses a standard type of configuration file format to set options for how the server should run and behave.  

SBA comes with a set of configuration files for different purposes.  However, you'll probably want to create your own configuration file to represent the settings of your machine and its display (see the [[Application]](#application) section below).

As mentioned in the server [setup](setup.html) page, the server can optionally take any number of additional config files.  This can be handy to use one config to keep your standard options and a second one to use for any game or activity of the day.

In fact the configuration examples provided with the server do just that and setup a 'machine' file to specify the size of the window and then a 'lesson' file to use for the activity of the day in class.

	SBA_Serv machine_test.cfg lesson_findthemiddle.cfg


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

*See the default.cfg file for the list of default configuration values.*


<a name="application"></a>[Application]
---------------------------------------
This section contains options pertaining to the graphical window created to run the SBA server.  It will affect how SBA is presented to you.

###fullscreen = boolean
Specifies whether or not SBA should run fullscreen or in a window.  **Note**: you should make sure that the horizontal and vertical resolutions match your displays resolution values OR you can set *both* **horz_res** and **vert_res** to **0** for your display resolution to be *automatically* detected.

###horz_res = integer
Specifies the horizontal resolution of the SBA window (in pixels).  This should match your monitor resolution if you plan to run the game in fullscreen.

###vert_res = integer
Specifies the vertical resolution of the SBA window (in pixels).  This should match your monitor resolution if you plan to run the game in fullscreen.

###sound = boolean
Determines if sounds should be played or not.

###showip = boolean
If this option is enabled, the server will start displaying the computer's IP Address at the top of the screen.  It can still be toggled manually on/off regardless of this setting with the [keyboard shortcut](usage.html).

###showstats = boolean
If this option is enabled, the server will start with some basic GUI options already enabled showing statistics about a player’s ship.

###ship_images = integer
This specifies the number of images that can be used for ships in the *GUI\Graphics\Ships* directory.  Use an existing ship image as a template to create more ship images.  Each frame of a ship should be contained in a 64x64 pixel square within the image.  The top row of images show a normal ship, the bottom a cloaked ship.  The first image is neutral, then left thruster firing, front thrusters, right thruster, back thruster, all thrusters (braking), and warping.


<a name="world"></a>[World]
---------------------------------------
This section contains options for how large the universe is.  These options should be set to be *at least* as large as the Screen options, but can be larger.  *It is generally recommended that they are each 1.5 or 2 times the value of their corresponding Screen values.*

###collisions = boolean
Turn collision detection on/off in the physics engine.  Useful for introductions to the world without worrying about actual interference.  **Note:** Most non-basic games won't work without this option on.

###width = integer
Horizontal length of the universe in pixels. *Alternately, you can specify "x" and a number to multiply the horizontal resolution value by your number for the world width.*

###height = integer
Vertical length of the universe in pixels. *Alternately, you can specify "x" and a number to multiply the vertical resolution value by your number for the world height.*

###radar_include_name = boolean
Determines if the name of the ship can be obtained through a Radar Command or not.


<a name="server"></a>[Server]
---------------------------------------
This section of options controls how the server should behave and accept connections from clients.

###port = integer
The TCP/IP port that the server should run on.  If this is changed from the default (**2012**), then a third parameter of a port number must be passed in when running the TextClient class from a Java client.

###multiple_connections = boolean
This option when enabled allows the same client machine to be connected to the server more than once.  Otherwise, each IP address is only allowed to connect a single time to a server instance.  This can cause issues if a client’s connection unexpectedly terminates.

###allow_re-entry = boolean
Can a player join the server again if they had connected previously and disconnected?

###disconnect_on_idle = boolean
Determines if a player's ship should be disconnected if it doesn't issue a command periodically (within 10 seconds of the last command being executed finishing).  **Note:** this will not prevent a ship from disconnecting if the actual socket is detected to be closed.

###disable_commands = string
Comma separated list of ship commands to disable on the server.  E.g.

	disable_commands = WarpCommand,FireTorpedoCommand
	
A list of commands can be found in the Command chapter. When a command is invoked that has been disabled, it is simply ignored. A message should return to the client, but they will get a new environment and their ship should continue running.  Its state might just not be what was expected.


<a name="spawnmanager"></a>Spawn Manager
---------------------------------------
Spawn Manager itself is not a specific configuration section.  It manages the life cycle for all the entities below.  Each entity has a set of common properties (listed here) which can be applied to them.  Place these properties within the specific [Entity] section for it to apply to that particular one.

E.g.

	# Spawns two Asteroids into the Universe, ensures there's always one
	[Asteroid]
	number = 2
	spawn_keep_min = 1

###number = integer
The number of [Entity] to generate in the universe.

###buffer_object = integer
Amount of space (in pixels) to leave between this object and all others when spawning it.

###buffer_edge = integer
Amount of space (in pixels) to leave between this object and the edge of space when spawning it.

###spawn_keep_min = integer
Minimum number of [Entity] to keep in the world.  If the number falls below this value, more entities will automatically be added instantly to meet this threshold.

###spawn_keep_max = integer
Maximum cut-off for spawning new [Entity] types on the timer.  If the number of objects has reached this level, no new entities will be spawned using the spawn timing settings below. Games or other events may still spawn entities of this type however.

###spawn_time_num = integer
Number of entities to spawn at a time with the timing settings below.  If specified, you must also specify the spawn_time_min and spawn_time_max options.

###spawn_time_min = integer
Minimum time in seconds before spawning the spawn_time_num of [Entity] unless spawn_keep_max has been reached.

###spawn_time_max = integer
Maximum time in seconds before spawning an [Entity] on a timer.

###spawn_alive_time_min = integer
###spawn_alive_time_max = integer
Specified together in order to cut-short the life span of an [Entity].  The [Entity] will live for a time between the range specified by these two values and then be automatically destroyed.

###spawn_on_player_num = integer
Number of [Entity] to add to the universe when a player is added to it.

###spawn_on_player_start = boolean
###spawn_on_player_respawn = boolean
Specify which scenarios (first created in round and/or whenever re-added) to add the spawn_on_player_num [Entity] to the world.

<a name="asteroid"></a>[Asteroid]
---------------------------------------
Asteroids are flying debris in space.  They start off with a set amount of momentum and will continue flying in space until impacting ships or destroyed by torpedos.


<a name="dragon"></a>[Dragon]
---------------------------------------
Dragons fly around space and will attack (and eat) nearby uncloaked ships.

###range_min = int
###range_max = int
Range for the size of the Dragon's visibility radius.  It will attack ships that enter this range centered on its head.

###attack_speed_min = int
###attack_speed_max = int
Range for the amount of speed a Dragon will increase by when it sees a Ship.

###attack_time_min = float
###attack_time_max = float
Range for the interval between times that the Dragon bites a Ship in its jaws.  This range is randomized for each attack.

###attack_amount_min = float
###attack_amount_max = float
Range for the amount of damage every bite causes a Ship.  This amount is randomized for each attack.

###health_min = int
###health_max = int
Range for the amount of health a Dragon will start with.


<a name="planet"></a>[Planet]
---------------------------------------
Planets have gravity wells which can pull ships towards them.  They are solid and will cause damage to ships that impact them.

###range_min = integer
see range_max

###range_max = integer
These two range values correspond to the distance away from a planet's center that its gravity field should pull ships in.  A random value will be generated between the **range_min** and **range_max** values.  These are typically **112** and **192**.

###pull_min = integer
see pull_max

###pull_max = integer
These two values correspond to the amount of pull the gravity will have on ships.  Larger values mean ships will get pulled in quicker and will have a harder time escaping.  A random value will be generated between **pull_min** and **pull_max**.  These are typically **8** and **24**.  Setting pull to zero, will turn off gravity.

###pull_torpedo = boolean
If enabled, Planets', BlackHoles', and Stars' gravity wells will effect torpedos.


<a name="blackhole"></a>[BlackHole]
---------------------------------------
Black Holes have stronger gravity wells than planets, but can be passed through their center.  They are harder to escape from.

They have the exact same configuration values as [Planets](#planet).  However, the default range values are **64** and **208**.  The default pull values are **52** and **72**.

###crush_time = float
Amount of time in seconds before a ship will be crushed (destroyed) when in the center of a black hole.  The Ship must be in the center for the whole duration to be crushed.  Shields will protect the ship from crushing as long as they are up.  Set to 0.0 to turn off crushing.  Defaults to **5.0**.


<a name="star"></a>[Star]
---------------------------------------
Stars can be flown into, but cause progressively more damage the closer a Ship is to its center.

They have the exact same configuration values as [Planets](#planet).  However, the default range values are **96** to **224**.  The default pull values are **12** to **48**.

###dmg_mod = float
Additional damage modifier for growth of damage caused by approaching Star's center.  Defaults to **0.0**.  Equation for damage calculation is currently in part *18 - (pull / 6.0) - dmg_mod*.


<a name="nebula"></a>[Nebula]
---------------------------------------
Nebulas are a celestial body which impart a drag effect on ships causing them to slow down or eventually stop if they are not thrusting.

###sizes = list of tuples
This is a list of the available sizes of nebulas.  The tuple pair is the total length of the **major** and **minor** axes of an ellipse.  There also needs to be a corresponding image in the *GUI\Graphics\Nebula* folder with the name **NebulaMAJORxMINOR** where 'MAJOR' and 'MINOR' are replaced with the values of the size of the Nebula.  These values should be placed in a list.  E.g.

	sizes=[(512,128),(384,256)]

###pull_min = integer
see pull_max

###pull_max = integer
These two values correspond to the amount of pull the drag will have on ships.  Larger values mean ships will slow down faster.  It'd best not to make these values higher than the Ship's Thruster force of 3500.  A random value will be generated between **pull_min** and **pull_max**.  These are typically **1750** and **2500**.  Setting pull to zero, will turn off drag.


<a name="wormhole"></a>[WormHole]
---------------------------------------
Worm Holes transport ships vast distances instantaneously.  Each particular Worm Hole will always behave in the same manner depending on its type.  It could always teleport you to a random location, a fixed location, or another worm hole entrance.  If exiting near an existing Worm Hole, you must leave its vicinity before entering again.

Extra Worm Holes above the number specified may be generated as two-way 'linked' Worm Holes.

###types = list of ints
This is a list of the types of Worm Hole exits which should be generated.  The following is a list of numbers and their corresponding type:

 1. Random
 2. Other Worm Hole
 3. Fixed Point

For instance the following would create Worm Holes which transport ships to random or fixed locations only:

	types=[1,3]

###buffer_exit_object = int
###buffer_exit_edge = int
Amount of space between objects/world edge to leave at exit of random/fixed point worm holes.  See (Spawn Manager)[#spawnmanager]'s similar properties.


<a name="game"></a>[Game]
---------------------------------------
Main options for the behavior of the simulation and which tournament rules should be applied.

###game = string
Name of the game to be played on the server.  See more info in the Competitions chapter about running games.

To just have a standard universe running, use **BasicGame**.

###auto_start = boolean
When set to true the game/round will automatically start when the server is run.  Otherwise, it will wait for you to press the space key.

This value is set to *false* if tournament is set to *true*.

###allow_after_start = boolean
Can players join the server after the game has already started?

###disconnect_on_death = boolean
Determines if a player will be completely disconnected from the server when they die.

###reset_score_on_death = boolean
Will a player's score reset to 0 when they die.

###points_lost_on_death = positive integer
Number of points a player loses when they die. Should be a **positive** integer or zero.

###points_initial = positive integer
Number of points each player should start with.  Should be a **positive** integer or zero.

###primary_victory_attr = string
This represents what the primary victory condition should be.  For basic games, this will either be **score** or **bestscore**.  Which either represents their current score or the best score they've achieved between deaths.  Other games may have other attributes which can be inspected.

###primary_victory_highest = boolean
Represents if the primary victory condition is sorted from highest to lowest (this is usually the case).

###secondary_victory_attr = string
This represents what should break ties on the primary victory condition.  For basic games, this is usually **deaths**, but could also be **bestscore** for instance.

###secondary_victory_highest = boolean
Represents if the secondary victory condition is sorted from highest to lowest.  For instance, if you wanted least deaths to be the tie-breaker, then you would set the secondary victory condition to be **deaths** and this value to be **false**.


<a name="tournament"></a>[Tournament]
---------------------------------------
Tournaments are run for more advanced games and divide players into groups to compete for a top score.  Then the top player from each round will advance to a final round.  This section defines settings related to running tournaments.  See more info in the Competitions chapter.

###tournament = boolean
Should the game be run in a tournament setting where connected players are split into a number of groups.  Each winner of the game in a group proceeds to a final bracket to determine a winner.  Each round will automatically be paired, timed, and calculated.  Just hit space to start each round.

###manager = string
Name of the Tournament Manager to use for controlling the tournament.  Current options are **BasicTournament** or **WildTournament**.  See [Tournaments](tournaments.html) page for more details.

###groups = integer
How many groups should the number of clients connected be broken into for the tournament?  E.g. Setting this value to 5 and having 30 clients connected would result in 5 rounds of 6 players each and a final round with the winners of each group.  Raising this number to higher values requires more vertical real-estate for the tournament display board.

###number_to_final_round = integer
How many players from each preliminary round should advance to the final round. i.e. The top X players will be taken into the final round where X is this options value.

###round_time = integer
How long each game round should last in seconds.

###reset_world_each_round = boolean
Should the world be cleared of all objects and recreated between each round of play?
