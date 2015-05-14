---
title: Lessons
outline-header: Lessons
outline:
 - { url: "#intro", title: "Intro & Connections" }
 - { url: "#findthemiddle", title: "Find The Middle" }
 - { url: "#shapesinspace", title: "Shapes in Space" }
 - { url: "#radar", title: "Intro to Radar" }
 - { url: "#competitions", title: "Competitions" }
---

Lessons
========
Space Battle Arena is a great environment to educate students about a variety of different topics.  Its main purpose is to help AP Computer Science students utilize the skills they've learned about all year in an interesting and engaging way.

The following lessons are provided as guidance towards a ***4 week curriculum*** involving Space Battle Arena.

Classroom Setup & Equipment
---------------------------
It is assumed that Space Battle will be run in a lab based setting with *each student having access to their own machine* running a Java 8 version of the [JDK](http://www.oracle.com/technetwork/java/javase/downloads/index.html). See [Client Setup](../client/index.html) for more information about the client configuration required - though **it is suggested** to have students link to the jar on a shared network resource, so pushing updates to students when updating the server is automatic just by refreshing the jar.

A teacher machine should be able to present and *project* to the front of the classroom so that all students can see the [server](../server/index.html)'s simulation of space.  This machine needs to be a Windows machine to run the server executable right now, unless you run from the Python source.

Lesson Plans
------------
Follow the link in the table below for a more complete lesson plan for that activity.

| Day Number | Lesson                    |
|------------|---------------------------|
|  1 - 2     | [Intro & Connections](intro.html)|
|  3 - 4     | [Find the Middle](findthemiddle.html)|
|  5 -  8    | [Shapes in Space](shapes.html)|
|  9 - 12    | Intro to Radar + Minigame |
| 13 +       | Competitions              |

<a name="intro"></a>Intro & Connections [Days 1 - 2]
-------------------
[Full Plan](intro.html)

[Client Setup](../client/index.html)

The first day of class should be an introduction to the project.  Discuss the notion of controlling a ship, not having direct access to code, and how the main client loop will work.  If there is time, you can start setting up the students environment.

By the second day you should be distributing the client package to students and walk them through creating a ship with a registration method which can connect to the server and rotate continuously.  By the end of class, all students should be able to connect to the server. 

<a name="findthemiddle"></a>Find The Middle [Days 3 - 4]
------------------
[Full Plan](findthemiddle.html)

[See Find The Middle Game](../games/findthemiddle.html)

Now that students are able to connect, the 3rd day should be spent going over commands (Rotate, Thrust, and Brake) and controlling a ship in space.  This is also a good point to talk about blocking vs. non-blocking commands. 

Then give the students the objective to get their ship from their spawning point to somewhere near the middle of the world.  They can use the parameters given to the register ship method to calculate the mid-point of the universe.  Aim for students to have accomplished this by the end of the next day. 

<a name="shapesinspace"></a>Shapes in Space [Days 5 - 8]
------------------
[Full Plan](shapes.html)

It turns out drawing turtle graphics in space is a lot harder than you would think.  The next exercise teaches students a familiar concept in a whole new way.  Space Battle provides a way to draw shapes on the screen.

This lesson works towards students getting more comfortable with maneuvering their ship by incrementally learning to draw different shapes such as rectangles, stars, spirals, and an octagon circumscribed around a square.

<a name="radar"></a>Intro to Radar [Days 9 - 12]
-----------------------
Once players are comfortable maneuvering their ships, they need to understand how to *see* the world around them and react to it.

**Radar** is the way that enables students to get extra information about the world around their ship.

The first day of this lesson should be about explaining how radar works, what information it provides, and how the programming paradigm changes slightly with having to react in the next getNextCommand call.

To aid in this activity most of the [Basic Games](../games/basic.html) can be configured to provide a challenge and motivation via scoring.

<a name="competitions"></a>Competitions [Days 13+]
-----------------------
[Competitions Index](../games/index.html)

After the lessons preceding this one, students should be comfortable with the system and be able to work on a ship to complete more complex sets of tasks.  This time can be used to introduce a final project where students must complete an objective and compete against their fellow students. 

At the end (for instance as a ‘final’) a tiered tournament can be run with the entire class where ships are broken into groups of 4-5 at random and face each other.  The winner from each round moves to a final round where a victor is determined.   

See the [Server Configuration](../server/config.html) Instructions for more info on running tournaments through the configuration file.  Sample configuration files for all competitions are provided. 
