---
title: Intro to Radar
nav:
 - { url: "index.html", title: "Lessons" }
outline-header: Lessons
outline:
 - { url: "#objective", title: "Objectives" }
 - { url: "#config", title: "Suggested Configuration" }
 - { url: "#resources", title: "Resources" }
 - { url: "#classroom", title: "Classroom Notes" }
 - { url: "#commands", title: "Commands Used" }
 - { url: "#api", title: "API Used" }
---

Intro to Radar
===============
Once players are comfortable maneuvering their ships, they need to understand how to *see* the world around them and react to it.

There are three subgames which can help with introducing radar:

- [Asteroid Miner](../games/asteroidminer.html) encourages a more combative stance
- [Hungry Hungry Baubles](../games/hungryhungrybaubles.html) encourages exploration
- [Survivor](../games/survivor.html) which encourages more avoidance.

Though most of the [Basic Games](../games/basic.html) can be configured to provide a challenge and motivation via scoring.

**Be sure to populate the world with enough obstacles to prevent students from just flying straight and hoping they don't hit anything.**

<a name="objective"></a>Objectives
---------------------------------
A student can write a ship which can navigate around space by avoiding obstacles and/or destroying them.

<a name="config"></a>Suggested Configuration
--------------------------------
An Asteroid Miner game configuration is provided in the server package:

    SBA_Serv machine_fullscreen.cfg basicgame_asteroid.cfg
 
As well as a Survivor game:

    SBA_Serv machine_fullscreen.cfg basicgame_survivor.cfg

Extra specifics on the configuration for each game can be found on their page.
 
<a name="resources"></a>Resources
------------------------------

 * [Asteroid Miner](../games/asteroidminer.html) 
 * [Hungry Hungry Baubles](../games/hungryhungrybaubles.html)
 * [Survivor](../games/survivor.html)
 
<a name="classroom"></a>Classroom Notes
--------------------------------
**Radar** is the way that enables students to get extra information about the world around their ship.

The first day of this lesson should be about explaining how radar works, what information it provides, and how the programming paradigm changes.

When a RadarCommand is returned in your getNextCommand, the *next* getNextCommand callback's Environment will contain a RadarResults object which can be retrieved with getRadar().

The **RadarResults** acts as an ArrayList of ObjectStatus.  It will contain information about all the objects that were around the ship within its [radar range](http://mikeware.github.io/SpaceBattleArena/client/java_doc/ihs/apcs/spacebattle/ObjectStatus.html#getRadarRange()).

A Radar Command has 5 different modes.  Each mode returns a varying level of information about the types of objects around the ship, but more details require more time to complete.

**It is important** to note that the *RadarResults* object is not cached, therefore the second call to getNextCommand after a RadarCommand will have a **null** getRadar() value, unless another RadarCommand was requested.  It is up to the student to decide to cache any information they wish to maintain about the objects in the world longer than a single callback.

    This is the #1 reason we see student's code fail due to a NullPointerException!

Radar is agnostic to the edges of the world; however, the client Point commands return information based on the absolute bounds of the world.  Therefore, an object detected in radar range, may be on the 'other' side of the world.  It is up to the ship to determine if it should head over the boundary of the world to wrap around as the quickest path.

At this time, starting to learn about advanced commands for maneuvering is important as well as energy management.  Warp and All Stop can be expensive, but critical to passing or avoiding dangerous objects.  Similarly Raise Shields and Torpedoes can be used to protect against collisions or engage other ships.

<a name="commands"></a>Commands Used
--------------------------------
[RadarCommand](http://mikeware.github.io/SpaceBattleArena/client/java_doc/ihs/apcs/spacebattle/commands/RadarCommand.html), [SteerCommand](http://mikeware.github.io/SpaceBattleArena/client/java_doc/ihs/apcs/spacebattle/commands/SteerCommand.html)

Advanced: [WarpCommand](http://mikeware.github.io/SpaceBattleArena/client/java_doc/ihs/apcs/spacebattle/commands/WarpCommand.html), [RaiseShieldsCommand](http://mikeware.github.io/SpaceBattleArena/client/java_doc/ihs/apcs/spacebattle/commands/RaiseShieldsCommand.html), [FireTorpedoCommand](http://mikeware.github.io/SpaceBattleArena/client/java_doc/ihs/apcs/spacebattle/commands/FireTorpedoCommand.html), [AllStopCommand](http://mikeware.github.io/SpaceBattleArena/client/java_doc/ihs/apcs/spacebattle/commands/AllStopCommand.html)

<a name="api"></a>API Used
-----------------------------
[getRadar](http://mikeware.github.io/SpaceBattleArena/client/java_doc/ihs/apcs/spacebattle/Environment.html#getRadar()), [RadarResults](http://mikeware.github.io/SpaceBattleArena/client/java_doc/ihs/apcs/spacebattle/RadarResults.html)
