---
title: Tournaments
nav:
 - { url: "index.html", title: "Server Information" }
outline-header: Outline
outline:
 - { url: "#overview", title: "Overview" }
 - { url: "#setup", title: "Setup" }
 - { url: "#basic", title: "Basic Tournament" }
 - { url: "#wild", title: "Wild Tournament" }
---

Tournaments
=================

<a name="overview"></a>Overview
-----------

Tournaments are a great option for the last day of using Space Battle Arena with a group.  They automatically split players up into groups and manage running multiple games in order to declare a Victor.

<a name="setup"></a>Setup
-----------------------------

A 'tournament.cfg' is provided with the server package, so the easiest way to start a basic tournament is to include it at the end of your current game configuration:

	SBA_Serv.exe game_baublehunt.cfg tournament.cfg
	
This will start your Bauble Hunt subgame in tournament mode.  See the [Configuration](config.html) section for the basic parameters involved with tournaments, and see the sections below for more advanced setups.

Once Space Battle Arena starts, all players should connect their Ships to the server at once.  You can use the player list to see all the connections.

**It is important for players to not disconnect during the course of the tournament.** Especially, if they're continuing to another round.

Once all players have joined.  Hit the 'Space' key to start the first round of the tournament.  The 'T' key in the GUI toggles the tournament display and the 'P' key can cycle the player list to show just the current round's players.


<a name="basic"></a>Basic Tournament
-----------------------------

The **BasicTournament** is the default tournament manager.  It splits players into a number of *groups* (provided in the settings, default 4) and advances the top X players from each round to a final round (X is configurable with *number_to_final_round* and defaults to 1).

After each initial round has completed, the final round is played with the seeded players, and a winner is crowned from the top of that pool.


<a name="wild"></a>Wild Tournament
-----------------------------

The **WildTournament** manager is the same as the Basic Tournament; however, there are two additional options available.  Configured by the following configuration section:

	[Wildcard]
	number = integer
	play_round = boolean
	
	
###number = integer
Number of wildcard slots to provide.  A wildcard is the top scoring players across all players which did **not** advance.  This can be across groups.  Scoring is still defined by the subgame which is being played.

###play_round = boolean
If set to true, after the preliminary rounds, but before the final, another 'Wildcard' round will be played with the number of wildcard players specified taken from the pool of non-seeded players.  The top players from this group will advance to the final group.

If set to false, the number of wildcard players will automatically be added to the final round after the preliminaries finish, but before the final round begins.
