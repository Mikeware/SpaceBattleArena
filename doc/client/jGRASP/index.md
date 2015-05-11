---
title: jGRASP Client Environment Setup
nav:
 - { url: "../index.html", title: "Client Setup" }
outline-header: Outline
outline:
 - { url: "#overview", title: "Overview" }
 - { url: "#environment", title: "Initial Environment Setup" }
 - { url: "#execution", title: "Execution Instructions" }
---

jGRASP Client Environment Setup
=====================

<a name="overview"></a>Overview
-----------

This document provides instructions for setting up the Java environment for developing code which controls a ship in the [Space Battle Arena](http://battlearena.mikeware.com/) (SBA) programming game.

These instructions were prepared for [jGRASP](http://www.jgrasp.org/) 1.8 and above.

<a name="environment"></a>Initial Environment Setup
-----------------------------

Create a Spaceship class:

<pre><code>import java.awt.Color;

import ihs.apcs.spacebattle.*;
import ihs.apcs.spacebattle.commands.*;

public class ExampleShip extends BasicSpaceship {
    public static void main(String[] args)
    {
        TextClient.run("127.0.0.1", new ExampleShip());
    }

    @Override
    public RegistrationData registerShip(int numImages, int worldWidth, int worldHeight)
    {
        return new RegistrationData("Example Ship", new Color(255, 255, 255), 0);
    }
    
    @Override
    public ShipCommand getNextCommand(BasicEnvironment env)
    {
        return new IdleCommand(0.1);
    }
    
    @Override
    public void shipDestroyed()
    {
    }
}
</code></pre>

1. Adjust Workspace Classpath under Settings -> PATH/CLASSPATH -> Workspace:

	![Classpath Settings](Classpath.png)
	
2. Add the **[gson-2.2.jar](http://github.com/Mikeware/SpaceBattleArena/blob/master/bin/gson-2.2.jar?raw=true)** and **[SpaceBattle.jar](http://github.com/Mikeware/SpaceBattleArena/blob/master/bin/SpaceBattle.jar?raw=true)** under the PATH -> CLASSPATHS tab using the New button:

	![Jars in Classpath](AddJars.png)
	
3. Save and Compile your class.

<a name="execution"></a>Execution Instructions
-------------------------

**Note: Do not terminate the program through the jGRASP UI; instead, click in the console window and type 'QUIT' to gracefully close the connection.**

1. Compile and run your class as normal.

2. Type 'QUIT' in the output window to disconnect your ship:

	![Output Window](Disconnect.png)
