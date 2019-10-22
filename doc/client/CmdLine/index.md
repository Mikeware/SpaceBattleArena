---
title: Command Line Client Environment
nav:
 - { url: "../index.html", title: "Client Setup" }
outline-header: Outline
outline:
 - { url: "#overview", title: "Overview" }
 - { url: "#environment", title: "Initial Setup" }
 - { url: "#execution", title: "Execution Instructions" }
---

Command Line Client Environment Setup
=====================

<a name="overview"></a>Overview
-----------

This document provides instructions for running ships on the command line using **javac** and **java**.

These instructions were prepared for Java 1.7 and above.

<a name="environment"></a>Initial Setup
-----------------------------

1. Create a Spaceship class:

    ```java
    import java.awt.Color;

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
    ```

2. Be sure to have the <?# ReleasePathLink "gson-2.2.jar" /?> and <?# ReleasePathLink "SpaceBattle.jar" /?> in a known location (e.g. a 'lib' subdirectory).
	
3. Open a Command Prompt.

<a name="execution"></a>Execution Instructions
-------------------------

**Note: Do not terminate the program with Ctrl+C; instead, type 'QUIT' to gracefully close the connection.**

1. Compile your code with the following command:

	```bash
    javac -cp lib\SpaceBattle.jar;lib\gson-2.2.jar ExampleShip.java
	```
	
2. Run your code with the following command:

	```bash
    java -cp lib\SpaceBattle.jar;lib\gson-2.2.jar;. ExampleShip
	```
	
	Note: the addition of the ';.' this is to represent the location of your compiled class file.

3. Type 'QUIT' in the console window to disconnect your ship.
