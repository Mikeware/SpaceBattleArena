---
title: Find The Middle
nav:
 - { url: "index.html", title: "Competitions" }
 - { url: "basic.html", title: "Basic Games" }
outline-header: Outline
outline:
 - { url: "#overview", title: "Overview" }
 - { url: "#config", title: "Configuration" }
---

Find The Middle [Basic Game]
=============

<a name="overview"></a>Overview
-----------

**Find the Middle** is a basic game which is a great first step into the world of Space Battle.  The objective is to navigate your ship to the center of the world.

The center can be determined through the parameters passed to you in the [registerShip](http://mikeware.github.io/SpaceBattleArena/client/java_doc/ihs/apcs/spacebattle/Spaceship.html#registerShip%28int,%20int,%20int%29) method.

<a name="config"></a>Configuration
-----------

###objective_radii = list[int]
Take a list of radius to put out from the center of the world as objectives.  Should be in increasing size. i.e. [50, 150, 300]

###objective_points = list[int]
Specifies how much each corresponding ring above is worth in number of points.  i.e. [4, 2, 1]

###objective_time = int
How long must a player remain at a low speed to collect the points.

###reset_timer = boolean
Should the objective timer reset if the ship's speed increases past the objective velocity again.

###objective_velocity = int
What speed is considered slow to start counting towards the **objective_time**.