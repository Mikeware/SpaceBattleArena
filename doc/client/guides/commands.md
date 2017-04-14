---
title: Ship Commands
nav:
 - { url: "index.html", title: "Space Battle Academy" }
---

Your spaceship is very advanced.  It can accept many different commands.  However, you may not need them all during your travels.

This reference guide describes the functions and uses of the different commands available.  See the complete manual for their usage and technical specifications [here](../java_doc/index.html?ihs/apcs/spacebattle/commands/package-summary.html).

The commands below will be essential to your ability to navigate space and control your ship:

> **Thrust** will fire the specified engine for the given duration with a percentage of the available thrust power.

> **Idle** will cause your ship to wait for the given period before updating the environment information and requesting a new command.

> **Brake** will slow your ship to a percentage of its current speed.

> **Rotate** your ship's orientation by a number of degrees. Positive rotations are counter-clockwise.

> **Steer** will adjust your ships movement direction (but not orientation) by the given amount.

> **Radar** is used to retrieve information about what's around your ship in the next callback.
