---
title: Basic Games
nav:
 - { url: "index.html", title: "Competitions" }
outline-header: Basic Games
outline:
 - { url: "findthemiddle.html", title: "Find The Middle" }
 - { url: "survivor.html", title: "Survivor" }
 - { url: "asteroidminer.html", title: "Asteroid Miner" }
 - { url: "combatexercise.html", title: "Combat Exercise" }
---

Basic Games
============
Basic games can be played with the default implementation of BasicSpaceship without having to worry about the generics or casting needed to play games passing back additional information.

All basic games use the [BasicGameInfo](http://mikeware.github.io/SpaceBattleArena/client/java_doc/ihs/apcs/spacebattle/BasicGameInfo.html) object provided in the [BasicSpaceship](http://mikeware.github.io/SpaceBattleArena/client/java_doc/ihs/apcs/spacebattle/BasicSpaceship.html) abstract class.  

This object contains common elements like a player's score, best score, number of deaths, or information about the game itself such as the highest score, the time left in the round, or the total time of the round.

Basic games also have a lot of configuration available through the [game configuration section](../server/config.html#game).
