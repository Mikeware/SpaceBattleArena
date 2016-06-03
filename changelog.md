v1.2 : Planned - May 2016 [Season 5] - The Hunger Baubles
----
* Added **The Hunger Baubles** Subgame
	* Bauble Games can now spawn any number of different valued Baubles.
	* Bauble Games can now spawn different weights of Baubles.
	* Added Worm Holes (teleports objects across space)
	* Added Deployable Space Mines
* Updated Client Angle/Point Methods
    * Orientations are always integers now and should be between 0-360
        * Rotate and Steer Command parameters updated
    * Movement direction can still be a double
    * Added Test Cases for Point Class
       * Fixed **getAngleTo** method to use built-in atan2
    * Added **isCloseTo** box test method
    * Added **getPointAt** for point projections based on angles and distance
    * Added **isInEllipse** check method
    * Added **getClosestMappedPoint** for world bounds assistance
* **ThrustCommand** now has a parameter to allow it to block.
* Added ability for client to get info on ship's running commands **getCommandQueue** in the environment *getShipStatus*.
	* Command Queue and Current Energy Properties are now only available to its own ship (can't be seen with radar).
* Updated Find the Middle Basic Game
	* Added new *reset_timer* option
	* Better Generation of Spawn Points and other Bug Fixes
* Added **Dragon's Lair** Basic Game (based on Survivor)
    * Dragons AI has been slightly improved
    * Asteroids and Dragons Initial Movement Speed can be Configured
    * Dragons highlight target in Debug mode
    * Added Ability for Points to be Generally Handled by Spawn Manager for Asteroids and Dragons for Torpedos and Ramming
* General Fixes/Improvements
	* *Optimized Network Code to half required Threads*
	* Spawn Manager fixed to only look at specific Type for evaluating min/max not Subclasses.
	* Added option for Torpedoes to be effected by gravity **pull_weapon**
	* Added **enable_commands** [Server] config option.
	* Split 'explodable' from 'gravitable' for Entities, two separate object flags now.
	* Can click ships in tracking mode to switch tracking to the clicked ship.
	* Separated option for 'showip' in Application settings to decouple from showing statistics, no longer always show IP in Debug mode.
	* 3 New Ship Graphics
	* Fixed issue with LowerEnergyScoopCommand and Dragons
	* Add Microsoft Message Analyzer Log Parser Support
* **Breaking Changes:**
    * Made **Hungry Hungry Baubles** a Basic Game by creating a *getObjectiveLocation()* method on BasicGameInfo (instead of *getGoldenBaublePosition()*).  This is now also used by **Bauble Hunt** and **Discovery Quest** instead of *getHomeBasePosition()*.
        * Hungry Hungry Baubles has new options for configuration (default is similar to previous incarnation).
        * Hungry Hungry Baubles and Bauble Hunt now share new *[BaubleGame]* point/percentage spawning parameters.
        * **Bauble Hunt** now respects weight not number carried for *ship_cargo_size*.  Default weights are set to 1 though to behave in same manner as previously.
        * *BaubleHuntGameInfo* has *getBaublesCarriedWeight* method now.
    * One Time Commands (AllStop, FireTorpedo) have been modified with cooldown times (i.e. **AllStopCommand** now waits for 5 seconds after stopping before returning).
    * RotateCommand/Orientation Related Client code now uses **int** vs. **double**.
    * Client code now does some validation of command arguments, can **throw IllegalArgumentException**.
    * **Removed SelfDestructCommand**
    * Game API: Removed **AsteroidMiner** as an example game, now configurable generally, config file for game still exists.
    * Game API: Player object now has **update_score** method instead of Game.

v1.1.0.1111 : 04/21/2016 [Season 4 Release] - Discovery Quest
----
* Added Build Numbers
* Replaced all sounds with Public Domain ones
* Added **Discovery Quest** Subgame
    * Subgames can create/intercept Commands
    * Simplified/Improved Subgame Physics handlers
        * Added *collidable* property
    * Radar methods know player who is radaring now
    * Cleaned up round start/end world life cycle management
        * Cleaned up object damage/life cycle management
            * AllStopCommand can destroy ship properly now
            * Cleaned up GUI player ship references
    * Spawn Manager
        * Dynamic GUI Object Spawning 
            * List Display with Mouse Wheel support
            * Middle-click performs action and remains in current mode
            * Right-click cancels mode
        * Controls timed spawning of objects
        * Controls minimum and maximum number of objects
        * Controls initial spawn parameters/world generation
            * Entities now have static spawn method (to be used by Spawn Manager)
        * Controls time to live of spawned objects
        * Controls spawning on player additions/respawns
    * Abstracted Tournament Management to separate class
        * Added 'Wild' Tournament which moves 'wildcard' players forward based on top scores across rounds.
    * Added Influential Body base class (something happens around it)
        * Added Dragons (chase ships)
    * Added Stars (players take damage the closer they are to their center)
        * Added Celestial Body base class (things happen within them)    
        * Made Black Holes crush ships within them for a period of time
* Ship Tracker HUD in GUI
    * Tracking now by player instead of ship
* Dynamic GUI Image Loader
* Aligned JavaDoc Version Numbers with Server
* **Breaking Changes:**
    * Renamed HomeBase to Outpost in Bauble Hunt to align with Discovery Quest
    * Changed shipDestroyed parameters in client interface

v1.0.1 : 05/26/2015 - Patch Release
----
* Added this changelog
* Functional Updates:
    * *SteerCommand* can also be **non-blocking** now (optional parameter)
    * *IdleCommand* costs **no** energy
    * Survivor game now based on travel to encourage movement.
    * *Auto-kick* feature for inactive clients (disconnect_on_idle)
    * Client prints statistics on exit
    * BasicSpaceship doesn't require shipDestroyed method any more
* General Client Disconnect and Threading Improvements
* Log files now append timestamp to name
* Fix issues with Planets and Nebulas
* Additional Celestial Body Graphics by Jeff
* Removed unneeded dependencies from Server build to save 1MB.

v1.0 : 05/11/2015 - [Season 4 Kick-off] Open Source + Improvements on Season 3 Build
----
* Open Sourced under GPLv2
* Re-architected subgame system on client and server, with new subgames:
    * King of the Bubble Game (and variant)
    * 'Basic' Games:
        * Find the Middle
        * Survivor
        * Asteroid Miner
        * Combat Exercise
* Nebulas (cause drag)
* [Steer Command](http://mikeware.github.io/SpaceBattleArena/client/java_doc/ihs/apcs/spacebattle/commands/SteerCommand.html)
* Improved Client Disconnect
* Improved Configuration Management
* Improved World Entity Class Hierarchy
* Improved Logging Format
* Added Unit Test Framework
* Stabilization and Bug Fixes
* [Website](http://mikeware.github.io/SpaceBattleArena/)

No Public Releases [Season 3] - King of the Bubble
----------
* King of the Bubble Game (2013-2014)

v0.9 : 09/11/2013 [Season 2] - Bauble Hunt/First Public Release
----
* 2nd Season (2012-2013) Package with 'Hungry Hungry Baubles' and 'Bauble Hunt' games.
* Introduction of *advanced* commands: All Stop, Cloak, Fire Torpedo, Raise Shields, Repair, Warp
* Migrate to PyMunk 3.0.0
* Detailed History Not Maintained

v0.1 - v0.75 : 05/08/2012 - 06/13/2012 [Season 1] - Baubles
------------
Space Battle Arena Begins, developed iteratively over the course of April, May, and June 2012.

'Hungry Hungry Baubles' (then Bauble Hunt) was the first competition.

Initial Commands: Thrust, Brake, Rotate, Idle, Radar, Deploy Laser Beacon, Destroy Laser Beacons