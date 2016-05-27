---
title: Competitions
outline-header: Competitions
outline:
 - { url: "basic.html", title: "Basic Games" }
 - { url: "findthemiddle.html", title: "Find The Middle" }
 - { url: "survivor.html", title: "Survivor" }
 - { url: "survivor.html#dl", title: "Dragon's Lair" }
 - { url: "asteroidminer.html", title: "Asteroid Miner" }
 - { url: "combatexercise.html", title: "Combat Exercise" }
 - { url: "hungryhungrybaubles.html", title: "Hungry Hungry Baubles" }
 - { url: "baublehunt.html", title: "Bauble Hunt" }
 - { url: "kingofthebubble.html", title: "King of the Bubble" }
 - { url: "kingofthebubble.html#kos", title: "King of Space" }
 - { url: "discoveryquest.html", title: "Discovery Quest" }
---

Competitions
============
Competitions provide a way to challenge students to complete objectives.  Some of these objectives may be simpler such as finding the center of the universe or trying to stay alive.  Others may be more complex and involve different strategies.

There are two classes of competitions.  Some competitions are ['basic'](basic.html) and only require the [BasicGameInfo](http://mikeware.github.io/SpaceBattleArena/client/java_doc/ihs/apcs/spacebattle/BasicGameInfo.html) object provided with the [BasicSpaceship](http://mikeware.github.io/SpaceBattleArena/client/java_doc/ihs/apcs/spacebattle/BasicSpaceship.html) abstract class.  This object contains common elements like a player's score, best score, number of deaths, or information about the game itself such as the highest score, the time left in the round, or the total time of the round.

Otherwise to play more advanced games, you'll need to implement the Spaceship<?> interface with the corresponding GameInfo object for the game being played (from the games package).

