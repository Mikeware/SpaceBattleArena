---
title: Server Usage / Shortcuts
nav:
 - { url: "index.html", title: "Server Information" }
outline-header: Outline
outline:
 - { url: "#overview", title: "Overview" }
 - { url: "#shortcuts", title: "Keyboard Shortcuts" }
 - { url: "#debug", title: "Debug Mode" }
 - { url: "#tracking", title: "Tracking Modes" }
 - { url: "#god", title: "'God' Modes" }
---

Server Usage / Shortcuts
================

<a name="overview"></a>Overview
-----------

The server is a graphical client which is a window into the universe and displays what is occurring.

It has many functions to help interpret what is occurring, manipulate the world, or display general types of information about games and tournaments.

The following information will explain keyboard shortcuts as well as various information about the different types of modes and features available.

<!-- Tables Generated with http://www.tablesgenerator.com/markdown_tables -->
<a name="shortcuts"></a>Keyboard Shortcuts
-----------------------------

### Display Toggles

| Key   	| Description               	|
|-------	|---------------------------	|
| **I** 	| IP Address                	|
| **P** 	| List of Connected Players/Players in Round 	|
| **S** 	| Stats on Objects          	|
| **N** 	| Name on Ships             	|
| **G** 	| Game Info                 	|
| **T** 	| Tournament Bracket        	|
| **R** 	| Round Time                	|

### General Keys

| Key       	| Description                                       	|
|-----------	|---------------------------------------------------	|
| **ESC**   	| Quit                                              	|
| **Space** 	| Start Game / Round (see *Game:autostart* setting) 	|

### Debug Keys

| Key   	| Description                                	|
|-------	|--------------------------------------------	|
| **D** 	| Debug Mode                                 	|
| **L** 	| In Debug Mode, Toggles Log Message Display 	|

### View Keys

| Key                    	| Description                                   	|
|------------------------	|-----------------------------------------------	|
| **Z**                  	| Toggle Zoom                                   	|
| **Up/Down/Left/Right** 	| Pan the View when Zoomed In                   	|
| **M**                  	| Toggle Scrolling with Mouse on Edge of Window 	|
| **MOUSEDOWN**          	| Zoom In / Re-center View                      	|

### Tracking Modes

| Key                 	| Description                  	|
|---------------------	|------------------------------	|
| **PageDown/PageUp** 	| Track Next/Previous Player  	|
| **END**             	| Stop Player Tracking         	|
| **Y**               	| Toggle Dynamic Ship Tracking 	|

### 'God' Commands

| Key   	| Description         	|
|-------	|---------------------	|
| **A** 	| Add Object Mode     	|
| **K** 	| Destroy Object Mode 	|
| **E** 	| Explosion Mode      	|
| **V** 	| Move Ship Mode      	|


<a name="debug"></a>Debug Mode
-----------------------------

Debug mode is useful for getting more insight into what may be occurring between some objects in the world.  Yellow circles show the Radar Range of ships.  Blue circles show the Gravity Wells of Planets and Black Holes.  Red lines from the ship show its Velocity vector.


<a name="tracking"></a>Tracking Modes
-----------------------------

Using PageUp/PageDown, you can select a specific player to track.  In this mode when zoomed in, the camera will continue to follow the specified player.  Also, in debug mode with logging turned on, only output for this ship will be shown.

When a player is being tracked, a display will be shown in the bottom-right corner with information about the ship's current status as well as the commands it is currently trying to execute.

The Dynamic camera mode will switch between ships to show whoever happens to have the highest score in the current game.


<a name="god"></a>'God' Modes
-----------------------------

There are four independent modes that allow you to manipulate the SBA world while it is running.  Left-Click will perform the action and exit out of the mode.  Middle-Click will perform the action but remain in the same mode (useful for performing the same action multiple times).  Right-Click will close whatever mode you're in.

The first command 'A' allows you to add objects such as Asteroids, Planets, Black Holes, and Bubbles (if playing King of the Bubble).  It can add any object which has been configured to be spawnable within the default Universe or the current game.  The Mouse Wheel can control scrolling through this list.

The next command 'K' allows you to click on any object in the world to destroy it.

The next command 'E' will cause an explosion force with the clicked location being the origin.  Everything within a nearby radius will have an outwardly force applied to it.

The finally command 'V' only works on whichever ship is currently being tracked (see above).  When activated, the ship will be moved to the clicked location.

