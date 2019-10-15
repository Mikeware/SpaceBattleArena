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

Combat Exercise [Basic Game]
=============

<a name="overview"></a>Overview
-----------

**Combat Exercise** is a basic game which introduces the notion of hunting other players.

Players must hunt for other players which are worth more points the longer they are alive.

Control asteroid spawning by using the standard [Spawn Manager](../server/config.html#spawnmanager) properties.

<a name="config"></a>Configuration
-----------

### points_time_alive_divide_by = int
Number to divide a player's time alive (in seconds) by to determine it's worth.  E.g. if this value was set to 1 and a player was alive for a minute, they'd be worth 60 points.  If it was set to 10 (default), then they'd be worth 6 points.

### points_shoot_asteroid = int
Number of points shooting an Asteroid with a torpedo is worth.
