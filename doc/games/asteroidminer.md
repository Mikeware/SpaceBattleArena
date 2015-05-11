---
title: Asteroid Miner
nav:
 - { url: "index.html", title: "Competitions" }
 - { url: "basic.html", title: "Basic Games" }
outline-header: Outline
outline:
 - { url: "#overview", title: "Overview" }
 - { url: "#config", title: "Configuration" }
---

Asteroid Miner [Basic Game]
=============

<a name="overview"></a>Overview
-----------

**Asteroid Miner** is a basic game which is a great way to introduce locating objects.

Players must destroy asteroids using torpedoes or by ramming into them with their ships.  Each asteroid is worth 2 points if destroyed with a torpedo or 1 point if rammed.

<a name="config"></a>Configuration
-----------

###points_torpedo = int
Number of points for destroying an asteroid with a torpedo.

###points_ship = int
Number of points for destroying an asteroid with a ship (without destroying your ship).

###spawn_time = int
How long between asteroid spawns.

###spawn_number = int
How many asteroids to spawn at the interval above.
