v1.2 : Planned - May 2016 [Season 5]
----

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