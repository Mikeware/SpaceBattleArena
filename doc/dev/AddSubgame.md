---
title: Adding a Subgame
nav:
 - { url: "index.html", title: "Development" }
---
Adding a Subgame to Space Battle
=====================

This document will explain how to add a custom Subgame to the Space Battle system.  Unfortunately, Space Battle can't be extended from an external library at this time, however, adding Subgames is relatively encapsulated and explained in detail below.

Server Implementation
--------------------------

Everything to drive your Subgame from the Server can be encapsulated into a single file.

1. Create a new .py file in the *Game* sub-folder in the Server project.

	It's easiest to start with an existing similar game as a template as many methods are required.  It's also suggested you inherit from the Basic Game which implements most of the base rules around how Space Battle works.

2. Make sure your file is named after your game and the name of your class is the name of your game + **Game**.  E.g. *AsteroidMiner.py* and *AsteroidMinerGame*

3. Create a config file where the rungame setting is set to the name of your game.  E.g. **AsteroidMiner**.

4. Read more about the specific game methods in the BasicGame documentation.

Client Implementation
-------------------------

If your game is *non-basic* (requires players have more information than Score, Highscore, and Deaths) perform the following steps:

1. Add a **GameInfo** class with a prefix of your game's name.  This can then be used when constructing a Spaceship as a Generic type.

2. In the *MwnpMessage.java* class, add to the switch statement in the *RegisterGameType* static method with the game name returned by the server as the string key and construct the appropriate *TypeToken* similar to the existing entries, but using your GameInfo class instead.

3.  It is recommended you reuse the existing game specific values on the **ObjectStatus**, such as *VALUE*, *NUMSTORED*, *HITRADIUS*, *OWNERID*, *NAME*.  If you require an additional property, add it here.  
  
	Note: The *NAME* property usually stores the NAME of a player, but this can be turned off in the Config file if you wish to not have a conflict/overlap and reuse it for some other purpose
	
	Remember that if you create a custom object, you have the full set of standard properties available as well, and the 'Type' property will be automatically populated with the Class name of your object from the Server.

4.  Add any new commands required for your game to the Commands package.

5. Recompile the SpaceBattle.jar.
