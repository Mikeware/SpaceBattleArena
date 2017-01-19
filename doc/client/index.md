---
title: Client Setup
outline-header: IDE Tutorials
outline:
 - { url: "jGRASP/index.html", title: "jGRASP" }
 - { url: "Eclipse/index.html", title: "Eclipse" }
 - { url: "BlueJ/index.html", title: "BlueJ" }
 - { url: "CmdLine/index.html", title: "Command Line" }
---

Client Setup
========
Any Java IDE should be able to be used for Space Battle Arena.

We typically use [jGRASP](http://www.jgrasp.org/) or [Eclipse](https://eclipse.org/).  Look to the **right** for some walk-throughs on setting up Space Battle using different IDEs.

The general process involves:

1. Adding both the Gson and SpaceBattle .jar files to your classpath.
2. Creating a Ship class which either extends the BasicSpaceship abstract class OR  
implements the Spaceship<?> interface.
3. Execute the TextClient's main method from the SpaceBattle.jar file with the following arguments:
    1. IP address of the server
    2. name of your Java Ship class

Alternatively, to the third step above, create a main method which calls the *run* method on TextClient with the IP Address and an instance of your Ship class.

If you need to run ships via the Command Line see [these instructions](CmdLine/index.html).

We also have a complete set of <a href="java_doc/" target="_blank">Java Docs</a> available.
