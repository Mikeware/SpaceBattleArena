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

Every player has an **Outpost** (locatable with *getObjectiveLocation()*) home base and baubles *only count* towards your score once they have been collected and **returned** to your Outpost.

You may store Baubles with up to a total weight of 5 on your ship.  (Baubles by default weigh 1.)
 
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

###bauble_weights = list[int]
List of weight values to use for Bauble Generation (defaults to 1).

###bauble_weight_percent = list[float]
Percentage that each of corresponding weighted baubles in the *bauble_weights* should appear.  Each value should be from [0.0-1.0].  The total of all weights provided in this list should equal 1.0.

###bauble_invert_ratio_percent = list[float]
Each float in this list corresponds to a value of bauble in the *bauble_points* list (i.e. you should have the same number of floats in this list as values of baubles).  The value [0.0-1.0] for each bauble specifies the percent chance that the weight percentage used from *bauble_weight_percent* is inverted (i.e. 0.8, 0.2 becomes 0.2, 0.8 for that bauble value).  E.g. set to 1.0 if you want the weight percentages to always be opposite for that value of bauble.  If this option is not specified, it will be set to 0.0 for all bauble values.


##[BaubleHunt]

###ship_cargo_size = int
The maximum weight of baubles each ship can carry.

###respawn_bauble_on_collect = boolean
Should a new bauble be spawned every time one is collected?
