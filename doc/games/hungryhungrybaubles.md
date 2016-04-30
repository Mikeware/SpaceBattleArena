---
title: Hungry Hungry Baubles
nav:
 - { url: "index.html", title: "Competitions" }
outline-header: Outline
outline:
 - { url: "#overview", title: "Overview" }
 - { url: "#config", title: "Configuration" }
---

Hungry Hungry Baubles
=============

<a name="overview"></a>Overview
-----------

**Hungry Hungry Baubles** is a game where you must try and collect as many baubles as you can before time runs out.

Every bauble is worth 1 point.

However, every player is also provided the location of a **golden** bauble.  If they collect it they will earn **5 points**.

If they happen to collect someone else's golden bauble it's only worth 3 points.

The default configuration also specifies that you lose 4 points when dying. See [[Game] Properties](../server/config.html#game).

Control Bauble spawning behavior by using the standard [Spawn Manager](../server/config.html#spawnmanager) properties.

<a name="config"></a>Configuration
-----------

###bauble_points_blue = int
How many points a standard blue bauble is worth. **Note:** *modifying the point values requires that adequate images be placed in the GUI/Graphics/Games folder to represent that value.*

###bauble_points_gold = int
How many points a golden bauble worth.

###bauble_points_extra = int
How many extra points is your specific golden bauble worth to you (doesn't require special image).
