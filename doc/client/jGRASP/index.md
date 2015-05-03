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
	
2. Add the **[gson-2.2.jar](http://github.com/Mikeware/SpaceBattleArena/blob/master/bin/gson-2.2.jar?raw=true)** and **[SpaceBattle.jar](http://github.com/Mikeware/SpaceBattleArena/blob/master/bin/SpaceBattle.jar?raw=true)** under the PATH -> CLASSPATHS tab:

	![Jars in Classpath](AddJars.png)
	
3. Save and Compile your class.

<a name="execution"></a>Execution Instructions
-------------------------

**Note: Do not terminate the program through the jGRASP UI; instead, click in the console window and type 'QUIT' to gracefully close the connection.**

1. Invoke a Static Method on a Named Class from the Build -> Java Workbench menu:

	![Invoke Static Method on Named Class](InvokeStatic1.png)
	
2. Type in a Class Name of 'ihs.apcs.spacebattle.TextClient' (in subsequent times, it should be selectable from the drop-down list):

	![Class Name ihs.apcs.spacebattle.TextClient](InvokeStatic2.png)
	
3. Select the main method in the list.

4. Type in the Parameters box the Server IP address and your *Java Class* name in quotes with a comma in-between (also selectable from the drop-down list in subsequent runs):

	![Invoke Method Dialog](InvokeStatic3.png)
	
	e.g. "127.0.0.1","ExampleShip"

5. Check the 'Don't Show Result Dialog'.

6. Hit the 'Invoke' button and then the 'Close' button.  

7. Type 'QUIT' in the output window to disconnect your ship:

	![Output Window](Disconnect.png)