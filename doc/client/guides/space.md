---
title: Space Coordinates
nav:
 - { url: "index.html", title: "Space Battle Academy" }
---

Space: The Final Frontier
========

In order to navigate your spaceship, you must be familiar with how to navigate within space.  There are a few different spatial concepts you should be aware of when navigating your ship through space:

 - Position
 - Direction
 - Orientation
 - Speed

Your **position** determines your location from the top-left of the universe.  That is your x coordinate increases to the right and your y coordinate increases down.

<img src="@(Context.Settings[Keys.LinkRoot])/img/coordinates.png" alt="Coordinate System" class="left indent"/> 

The **direction** of your spaceship doesn't have to match the **orientation** of it (i.e. you can be moving in one direction and facing to fire or thrust in another direction).  This allows for complex maneuvers and combat.  The angle for these two values will always be in degrees.  

<img src="@(Context.Settings[Keys.LinkRoot])/img/DirectionOrientation.png" alt="Direction vs. Orientation" class="left indent"/> 

> 0 degrees faces right.  

> Counter-clockwise movement is positive, clockwise movement is negative.

The ship's **speed** is always relative to its direction.  It is given in a value per second.  

> E.g.  If you're at position (100,100) and moving in direction 0 (right) at a speed of 10, after 5 seconds (assuming no acceleration or deceleration or other factors), you'd be approximately at position (150, 100).
	
Due to the real-time nature of the system, networking factors, and delays in processing, it will be impossible to know your exact location, react to an exact location, or precisely time maneuvers.  It is best to remember this when planning how to instruct your ship to react to different scenarios and how to plan out complex sets of instructions.  

After you are capable of handling basic ship manuevers, if you want to better perfect combatative scenarios, think about anticipating the locations of moving targets.

The other thing to note is that Space has no boundaries.  You can travel infinitely in any direction.  However,  you will 'loop' and encounter the same objects if you traverse parallel to an axis.   This is simulated by making Space a [torus](https://en.wikipedia.org/wiki/Torus).  Thus, if you encounter the minimum or maximum boundary of a dimension, you will immediately travel to the other side of that dimension.
