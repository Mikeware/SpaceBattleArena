---
title: Client Setup
outline-header: IDE Tutorials
outline:
 - { url: "jGRASP/index.html", title: "jGRASP" }
 - { url: "Eclipse/index.html", title: "Eclipse" }
---

Client Setup
========
Any Java IDE should be able to be used for Space Battle Arena.

We typically use [jGRASP](http://www.jgrasp.org/) or [Eclipse](https://eclipse.org/).  Look to the **left** for some walk-throughs on setting up Space Battle using different IDEs.

The general process involves:

1. Adding both the Gson and SpaceBattle .jar files to your classpath.
2. Creating a Ship class which either extends the BasicSpaceship abstract class OR  
implements the Spaceship<?> interface.
3. Executes the TextClient's main method from the SpaceBattle.jar file with the following arguments:
    1. IP address of the server
    2. name of your Java Ship class
