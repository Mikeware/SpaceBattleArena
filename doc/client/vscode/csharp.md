---
title: VS Code C Sharp Client Environment Setup
nav:
 - { url: "../index.html", title: "Client Setup" }
outline-header: Outline
outline:
 - { url: "#overview", title: "Overview" }
 - { url: "#csharp", title: "Initial C# Setup" }
 - { url: "#environment", title: "Initial Environment Setup" }
 - { url: "#classsetup", title: "Class Setup" }
 - { url: "#execution", title: "Execution Instructions" }
---

VS Code C# Client Environment Setup
=====================

<a name="overview"></a>Overview
-----------

This document provides instructions for setting up the C# environment for developing code which controls a ship in the [Space Battle Arena](http://battlearena.mikeware.com/) (SBA) programming game.

**This initial C# support was added by the community and is built by them, it is not yet officially supported by Mikeware, use at your own risk.** [See Issue #162](https://github.com/Mikeware/SpaceBattleArena/issues/162)

These instructions were prepared for [VS Code](http://code.visualstudio.com/) 1.39 and above.

<a name="csharp"></a>Initial C# Setup
-----------------------------

These instructions were tested with [.NET Core 3.0](https://dotnet.microsoft.com/download)

1. Download and install the [.NET 3 Core SDK](https://dotnet.microsoft.com/download), if you haven't already.

2. Open VS Code and Install the **C#** extension: `ms-vscode.csharp`

<a name="environment"></a>Initial Environment Setup
-----------------------------

1. Create a new folder and open it in VS Code.

2. Open the Terminal and type:

	```
	dotnet new console
	```

3. Then add the SBA NuGet package:

	```
	dotnet add package SBA_Client.Net
	```

<a name="classsetup"></a>Class Setup
----------------------

1. Open up the **Program.cs** file.

2. Modify it to look like this:	

<pre><code>using System;
using System.Collections.Generic;
using System.Drawing;
using SpaceBattleArena;

namespace APCS
{    
    class Program
    {
        static void Main(string[] args)
        {
            TextClient<BasicGameInfo>.run("127.0.0.1", new MyShip(), 2012);
        }
    }

    class MyShip : BasicSpaceship 
    {
	    override public RegistrationData registerShip(int numImages, int worldWidth, int worldHeight)
        {
            return new RegistrationData("Example Ship", Color.White, 0);
        }

    	override public ShipCommand getNextCommand(BasicEnvironment env)
        {
            return new IdleCommand(1);
        }
    }
}

</code></pre>
	
<a name="execution"></a>Execution Instructions
-------------------------

**Note: Do not terminate the program through the VS Code UI; instead, click in the Terminal window and use 'Ctrl+C' to gracefully close the connection.**

1. In your **Program.cs** file, edit the IP address in the call to TextClient.run to point it to the location of your server.

	```
	TextClient<BasicGameInfo>.run("127.0.0.1", new MyShip(), 2012);
	```

2. Open the Terminal and use:

	```
	dotnet run
	```

	To start the application.

3. Type 'Ctrl+C' in the **Terminal** pane to disconnect your ship.
