v1.0.1 : 05/??/2015
----
* Added this changelog
* Functional Updates:
  * *SteerCommand* can also be **non-blocking** now (optional parameter)
  * *IdleCommand* costs **no** energy
  * Survivor game now based on travel to encourage movement.
  * *Auto-kick* feature for inactive clients (disconnect_on_idle)
  * Client prints statistics on exit
  * BasicSpaceship doesn't require shipDestroyed method any more
  * Point class now has ** and ** helper methods
* General Client Disconnect and Threading Improvements
* Log files now append timestamp to name
* Fix issues with Planets and Nebulas
* Additional Celestial Body Graphics by Jeff

v1.0 : 05/11/2015 [Season 4] - Open Source
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

No Public Releases [Season 3]
----------
* King of the Bubble Game (2013-2014)

v0.9 : 09/11/2013 [Season 2] - First Public Release
----
* 2nd Season (2012-2013) Package with 'Hungry Hungry Baubles' and 'Bauble Hunt' games.
* Introduction of *advanced* commands: All Stop, Cloak, Fire Torpedo, Raise Shields, Repair, Warp
* Migrate to PyMunk 3.0.0
* Detailed History Not Maintained

v0.1 - v0.75 : 05/08/2012 - 06/13/2012 [Season 1]
------------
Space Battle Arena Begins, developed iteratively over the course of April, May, and June 2012.

'Hungry Hungry Baubles' (then Bauble Hunt) was the first competition.

Initial Commands: Thrust, Brake, Rotate, Idle, Radar, Deploy Laser Beacon, Destroy Laser Beacons