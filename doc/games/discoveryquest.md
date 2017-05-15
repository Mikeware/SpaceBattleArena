---
title: Discovery Quest
nav:
 - { url: "index.html", title: "Competitions" }
outline-header: Outline
outline:
 - { url: "#overview", title: "Overview" }
 - { url: "#config", title: "Configuration" }
---

Discovery Quest
=============

<a name="overview"></a>Overview
-----------
**Discovery Quest** is an exploration game where players must navigate space in order to 'scan' objects and accumulate points.  They establish a research **Outpost** which can also provide them with specific missions for additional points.
 
Players must establish an **Outpost** by scanning it before any points will count towards their placement within the game.  Any points earned prior to establishing an Outpost will be banked and awarded when an Outpost is first established. (Multiple players may establish and share the same Outpost.)  An established Outpost's location can be later retrieved with the *getObjectiveLocation()* method of the environment's getGameInfo().  *This can be turned off with configuration such that any objects scanned will receive points.*

*Scanning* is a specific command that must be used within 150 pixels of an object and must be directed towards a specific object by using its ID number.  Scanning is **not** the same as Radar.  The object being scanned must remain in range for the entire duration of the scan.

A **Mission** dictates which objects a ship should go scan.  If a ship goes and scans ***ONLY*** those things, bonus points will be awarded when they return to their outpost and Scan it again.  Scanning your Outpost will always give you a new mission.  **Note:** the first Outpost you scan becomes your base and is the only Outpost you can receive and complete missions from.  (Other Outposts may still be scanned for points or mission objectives.)

Your Ship being destroyed clears/fails your mission, so you must return to your established Outpost if you want a new one.

**NOTE: Discovery Quest prevents warping out of Nebulas, unless turned off in configuration.**


<a name="config"></a>Configuration
-----------
###establish_homebase = boolean
Whether or not the player must scan an Outpost first in order to start banking points. When off, all points scanned will count, Outposts can still be scanned for points and bonus missions if missions are enabled (see below).

###scan_time = float
Amount of time required to complete a successful scan in seconds. (3.5 default)

###scan_range = int
Distance required to be in range for a scan in pixels. (150 default)

###ship_spawn_dist = int
Maximum distance a ship will spawn away from an Outpost.

###disable_warp_in_nebula = boolean
Set to prevent players from Warping out of Nebulas. (true default)

###missions = boolean
Whether or not missions can be obtained from scanning outposts.

###mission_objectives = string
Comma separated list of object types which can appear within Missions.

###mission_num_min = int
Minimum number of objectives for a Mission to contain. (1 default)

###mission_num_max = int
Maximum number of objects for a Mission to contain. (3 default)

###mission_bonus_multiplier = float
Multiplier to apply to set of mission objectives and add to the player's score when the mission is completed. (3.0 default)

###points_asteroid = int
Number of points an Asteroid is worth when successfully scanned. (2 default)

###points_planet = int
Number of points a Planet is worth when successfully scanned. (2 default)

###points_blackhole = int
Number of points a Black Hole is worth when successfully scanned. (3 default)

###points_nebula = int
Number of points a Nebula is worth when successfully scanned. (1 default)

###points_star = int
Number of points a Star is worth when successfully scanned. (3 default)

###points_outpost = int
Number of points an Outpost is worth when successfully scanned. (2 default)  Establishing your own Outpost is worth double points.

###points_dragon = int
Number of points a Dragon is worth when successfully scanned. (6 default)

###points_wormhole = int
Number of points a Worm Hole is worth when successfully scanned. (2 default)

###points_ship = int
Number of points another Ship is worth when successfully scanned. (4 default)

###points_spacemine = int
Number of points a Space Mine is worth when successfully scanned. (8 default)
