---
title: Hungry Hungry Baubles
nav:
 - { url: "index.html", title: "Competitions" }
 - { url: "basic.html", title: "Basic Games" }
outline-header: Outline
outline:
 - { url: "#overview", title: "Overview" }
 - { url: "#config", title: "Configuration" }
---

Hungry Hungry Baubles [Basic Game]
=============

<a name="overview"></a>Overview
-----------

**Hungry Hungry Baubles** is a basic game where you must try and collect as many baubles as you can before time runs out.

Every bauble is worth at least 1 point.

However, every player is also provided the location of a **golden** bauble (added specifically for them outside of spawning parameters).  If they collect it they will earn **5 points** (3 + 2 additional, if enabled).

If they happen to collect someone else's golden bauble it's only worth 3 points.

Red Baubles are worth 5 points (if enabled, see **bauble_percent_red**).

The default configuration also specifies that you lose 4 points when dying. See [[Game] Properties](../server/config.html#game).

Control Bauble spawning behavior by using the standard [Spawn Manager](../server/config.html#spawnmanager) properties.

<a name="config"></a>Configuration
-----------

##[BaubleGame]

### bauble_points = list[int]
List of points each progressive bauble is worth. **Note:** *modifying the point values requires that adequate images be placed in the GUI/Graphics/Games folder to represent that value.*

### bauble_percent = list[float]
The percentage of baubles which should generate as the corresponding value.  Each value should be from [0.0-1.0].  The total of all values provided in this list should equal 1.0.


## [HungryHungryBaubles]

### assign_specific_bauble = boolean
Assign each player a golden bauble to retrieve given through *getObjectiveLocation()* in the environment's *getGameInfo()*.  Defaults to true.

### bauble_extra_value = int
How many points the 'golden' bauble is worth if you collect someone else's.  Only used if **assign_specific_bauble** is turned on.

### bauble_points_extra = int
How many extra points is your specific golden bauble worth to you (doesn't require special image).  Only used if **assign_specific_bauble** is turned on.
