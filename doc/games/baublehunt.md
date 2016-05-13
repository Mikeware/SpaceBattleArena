---
title: Bauble Hunt
nav:
 - { url: "index.html", title: "Competitions" }
outline-header: Outline
outline:
 - { url: "#overview", title: "Overview" }
 - { url: "#config", title: "Configuration" }
---

Bauble Hunt
=============

<a name="overview"></a>Overview
-----------
**Bauble Hunt** is a more complex version of the [Hungry Hungry Baubles](hungryhungrybaubles.html) game.  

Every player has a **home base** (locatable with *getObjectiveLocation()* and baubles *only count* towards your score once they have been collected and returned to your Home Base.

You may store 5 Baubles on your ship at most.
 
Blue Bauble are worth 1 point.
Golden Baubles are worth 3 points.
Red Baubles are worth 5 points.

If your ship is destroyed, the Baubles it was carrying will be dropped.

You will be provided a list of locations for where valuable baubles are located.

In the case of a tie, who ever has the fewest baubles collected will be the winner (i.e. density of points is rewarded in a tie).

Control Bauble spawning behavior by using the standard [Spawn Manager](../server/config.html#spawnmanager) properties.

<a name="config"></a>Configuration
-----------

##[BaubleGame]

###bauble_points = list[int]
List of points each progressive bauble is worth. **Note:** *modifying the point values requires that adequate images be placed in the GUI/Graphics/Games folder to represent that value.*

###bauble_percent = list[float]
The percentage of baubles which should generate as the corresponding value.  Each value should be from [0.0-1.0].  The total of all values provided in this list should equal 1.0.


##[BaubleHunt]

###ship_cargo_size = int
The maximum number of baubles each ship can carry.

###respawn_bauble_on_collect = boolean
Should a new bauble be spawned every time one is collected?
