---
title: The Hunger Baubles
nav:
 - { url: "index.html", title: "Competitions" }
outline-header: Outline
outline:
 - { url: "#overview", title: "Overview" }
 - { url: "#config", title: "Configuration" }
---

The Hunger Baubles
=============

<a name="overview"></a>Overview
-----------
**The Hunger Baubles** is a more complex version of the [Bauble Hunt](baublehunt.html) game.  

The Hunger Baubles are a game where you must hunt for the best collection of baubles.

Baubles have varying values and weights, and your ship can only carry so many.  You must use the Collect and Eject commands effectively in order to pick and choose your baubles.
 
Your cargo hold has a maximum weight capacity of 25.

 - Blue Baubles are worth 1 point.
 - Green Baubles are worth 2 points.
 - Golden Baubles are worth 3 points.
 - Orange Baubles are worth 4 points.
 - Red Baubles are worth 5 points.
 - Purple Baubles are worth 6 points.
 - Cyan Baubles are worth 7 points.

If your ship is destroyed, the Baubles it was carrying will be dropped.  However, your score is the best score you've achieved.  In the case of a tie, who ever has the fewest baubles collected will be the winner (i.e. density of points is rewarded in a tie).

**All ships** start at the edge of the Cornucopia (yellow circle).  The Cornucopia will spawn high-value baubles near its center as long as there are no ships within it.  It can also start with some initial bauble treasure (see config below).

The Cornucopia is protected by Dragons, if a ship is detected when it is trying to spawn a bauble, a Dragon will be spawned instead.

Asteroids and Dragons can be destroyed with Torpedos and may drop a bauble.

Control Bauble spawning behavior by using the standard [Spawn Manager](../server/config.html#spawnmanager) properties.

<a name="config"></a>Configuration
-----------

##[BaubleGame]

###bauble_points = list[int]
List of points each progressive bauble is worth. **Note:** *modifying the point values requires that adequate images be placed in the GUI/Graphics/Games folder to represent that value.*

###bauble_percent = list[float]
The percentage of baubles which should generate as the corresponding value.  Each value should be from [0.0-1.0].  The total of all values provided in this list should equal 1.0.

###bauble_weights = list[int]
List of weight values to use for Bauble Generation (defaults to 1).

###bauble_weight_percent = list[float]
Percentage that each of corresponding weighted baubles in the *bauble_weights* should appear.  Each value should be from [0.0-1.0].  The total of all weights provided in this list should equal 1.0.

###bauble_invert_ratio_percent = list[float]
Each float in this list corresponds to a value of bauble in the *bauble_points* list (i.e. you should have the same number of floats in this list as values of baubles).  The value [0.0-1.0] for each bauble specifies the percent chance that the weight percentage used from *bauble_weight_percent* is inverted (i.e. 0.8, 0.2 becomes 0.2, 0.8 for that bauble value).  E.g. set to 1.0 if you want the weight percentages to always be opposite for that value of bauble.  If this option is not specified, it will be set to 0.0 for all bauble values.


##[TheHungerBaubles]

###ship_cargo_size = int
The maximum number of baubles each ship can carry.

###respawn_bauble_on_collect = boolean
Should a new bauble be spawned every time one is collected?

###cornucopia_radius = int
How big should the cornucopia area be.  If your ship's position is within this radius distance from the cornucopia position, the cornucopia won't spawn baubles. (Note the visual ring on screen is slightly smaller so it looks like the edge of your ship needs to cross - though it is calculated like everything else by midpoints.)

###cornucopia_buffer_edge = int
What's the closest the cornucopia should be from the edge of the world.

###cornucopia_buffer_object = int
What's the closest the cornucopia should be from the edge of other objects.

###collect_radius = int
How far can a bauble be away from the ship for the Collect Command to pick it up.

###limit_weapons = boolean
Should each player be limited to having one torpedo and one space mine in the world at a time?

###cornucopia_spawn_initial_num = int
How many baubles should be spawned in the Cornucopia at the start of each round.

###cornucopia_spawn_keep_max = int
How many baubles should remain in the Cornucopia.  Baubles over this number which have remained in the Cornucopia the longest will be removed when the timer goes off (see below).

###cornucopia_spawn_time_num = int
How many baubles should spawn when the timer expires and there are no ships in the Cornucopia.

###cornucopia_spawn_time_min = int
What's the minimum random time to elapse before trying to spawn baubles in the Cornucopia.

###cornucopia_spawn_time_max = int
What's the maximum random time to elapse before trying to spawn baubles in the Cornucopia.

###cornucopia_spawn_points = list[int]
What value of baubles should spawn in the Cornucopia?  These values must exist in the **bauble_points** list.  The same weight percentages will be used as the general configuration however the bias per value within the Cornucopia will be uniform.

###cornucopia_spawn_dragon = boolean
Should the Cornucopia spawn a dragon at the Cornucopia position if a ship is detected instead when it tries to spawn a Bauble?

###cornucopia_spawn_initial_dragons = int
How many Dragons should initially spawn in the Cornucopia?

###cornucopia_spawn_max_dragons = int
How many Dragons should be allowed in the Cornucopia?  A new Dragon won't be spawned for ships if this number is reached and the Dragons remain within the Cornucopia.

###asteroid_bauble_percent = float
Percent Chance [0.0-1.0] that a Bauble is dropped when a player torpedos an Asteroid.

###asteroid_bauble_points = list[int]
Uniform set of values for baubles to spawn on asteroid destruction.  Value must exist in **bauble_points** list.

###dragon_bauble_percent = float
Percent Chance [0.0-1.0] that a Bauble is dropped when a player torpedos an Dragon.

###dragon_bauble_points = list[int]
Uniform set of values for baubles to spawn on dragon destruction.  Value must exist in **bauble_points** list.
