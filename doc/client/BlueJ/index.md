---
title: BlueJ Client Environment Setup
nav:
 - { url: "../index.html", title: "Client Setup" }
outline-header: Outline
outline:
 - { url: "#overview", title: "Overview" }
 - { url: "#environment", title: "Initial Environment Setup" }
 - { url: "#classsetup", title: "Class Setup" }
 - { url: "#execution", title: "Execution Instructions" }
---

BlueJ Client Environment Setup
=====================

<a name="overview"></a>Overview
-----------

This document provides instructions for setting up the Java environment for developing code which controls a ship in the [Space Battle Arena](http://battlearena.mikeware.com/) (SBA) programming game.

These instructions were prepared for [BlueJ](http://www.bluej.org/) (3.1.5) and above.

<a name="environment"></a>Initial Environment Setup
-----------------------------

1. From the **Tools** menu select **Preferences** in the main window:

	![Tools Preferences](PreferencesMenu.png)

2. Click on the **Libraries** tab.	

3. Click on **Add**.

4. Select both the <?# ReleasePathLink "gson-2.2.jar" /?> and <?# ReleasePathLink "SpaceBattle.jar" /?> which you should have downloaded:

	![Libraries Tab](LibrariesTab.png)
	
5. Click **OK**

6. Click **OK** on the warning that pops up:

	![Warning](Warning.png)
	
7. **Close and re-open BlueJ**.

<a name="classsetup"></a>Class Setup
----------------------

1. Click the **New Class...** button to add one to your project:

	![Add Class](AddClass.png)
	
2. Double-click the new class to bring up the editor and extend BasicSpaceship, like the example below:

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
    
}
</code></pre>

You should be able to go to Tools -> Compile (Ctrl-K) and have no errors.
	
<a name="execution"></a>Execution Instructions
-------------------------

**Note: Do not terminate the program through the BlueJ UI; instead, click in the console window and type 'QUIT' to gracefully close the connection.**

1. Go to your main window and right-click on your class.
	
2. Select the main method:

	![Run main](RunMain.png)
	
3. Click OK in the Method Call dialog which appears.

4. When done, type 'QUIT' in the **Console** window to disconnect your ship:

	![Output Window](Disconnect.png)
