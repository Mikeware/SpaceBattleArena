---
title: Home
layout: home
---

Space Battle Arena
============

Space Battle Arena is a ‘[Programming Game](http://en.wikipedia.org/wiki/Programming_game)‘ where you must write code (in Java) to autonomously control a space ship to accomplish specified objectives.  

<iframe width="560" height="315" src="https://www.youtube.com/embed/dfMpFtCXoQM?controls=0&showinfo=0&rel=0&modestbranding=1" frameborder="0" allowfullscreen class="right"></iframe>

This has been a final project used in an Advanced Placement High School Computer Science course since 2012.  Students have been enthusiastic, excited, challenged, and engaged with learning to control a ship in a physical environment and comparing strategies against their fellow students in a fun competition.

The question of why ‘Space Battle’ over an existing platform (like [Robocode](http://robocode.sourceforge.net/)) was brought up during our [Reach for the Stars](http://www.mikeware.com/2012/09/reach-for-the-stars-educating-the-next-generation-using-games/) talk.  The answer is that most programming games are built around a specific objective.  This means that while there may be varying strategies, eventually the problem can be solved and solutions available.  

In addition, it means the challenge is fixed and always the same.  For an educational context specifically, where this is most students first exposure to a 'third-party' library.  We wanted a system which could ease them into new concepts that build on what they had learned throughout the course of the year.  

Finally, allowing the system to be extensible and configurable, means that challenges and difficulty can be directly geared to a specific group of students abilities which can fluctuate from class to class.  Space Battle was our test bed and has proved successful with the multiple different challenges we have run over the past few years.

Space Battle Arena is [licensed](https://github.com/Mikeware/SpaceBattleArena/blob/master/LICENSE) under the GPLv2.  [Gson](https://github.com/google/gson) is licensed under the Apache license and provided for convenience alongside the release.

Student Environment
-------------------------
It is expected that students have completed a full year of Java programming in high school or just over a semester of programming at the college level.

We use [jGRASP](http://www.jgrasp.org/) as our IDE of choice when working with High School students, but any Java IDE can be used that is capable of adding a jar to a classpath and executing a class from within the jar as the main class.

Documentation
------------------
* [Client Setup](client/index.html)
    * [BlueJ](client/BlueJ/index.html)
    * [Command Line](client/CmdLine/index.html)
    * [Eclipse](client/Eclipse/index.html)
    * [jGRASP](client/jGRASP/index.html)
    * [VS Code](client/vscode/index.html)
    * [VS Code (CSharp)](client/vscode/csharp.html) [Community Driven]
* <a href="client/java_doc/" target="_blank">Java Docs</a>
* [Guides](client/guides/index.html)
    * [Coordinates](client/guides/space.html)
    * [Maneuvering](client/guides/maneuvering.html)
    * [Your Ship](client/guides/ship.html)
    * [Ship Commands](client/guides/commands.html)
    * [Celestial Objects](client/guides/objects.html)
    * [Ship Image Index](https://github.com/Mikeware/SpaceBattleArena/tree/master/SBA_Serv/GUI/Graphics/Ships)
* [Server Information](server/index.html)
    * [Server Setup](server/setup.html)
        * [Mac OS X Server from Source](https://github.com/Mikeware/SpaceBattleArena/blob/master/SBA_Serv/README.md)
    * [Server Config](server/config.html)
    * [Server Usage/Shortcuts](server/usage.html)
    * [Tournaments](server/tournaments.html)
* [Lessons](lessons/index.html)
    * 00 - [Intro and Setup](lessons/intro.html)
    * 01 - [Find the Middle](lessons/findthemiddle.html)
    * 02 - [Shapes in Space](lessons/shapes.html)
    * 03 - [Intro to Radar](lessons/radar.html)
    * 04 - Finite State Machines
    * 05 - Competitions
* [Competitions](games/index.html)
    * ['Basic' Games](games/basic.html)
        * [Find The Middle](games/findthemiddle.html)
        * [Survivor](games/survivor.html)
            * [Dragon's Lair (Variant)](games/survivor.html#dl)
        * [Asteroid Miner](games/asteroidminer.html)
        * [Combat Exercise](games/combatexercise.html)
    	* [Hungry Hungry Baubles](games/hungryhungrybaubles.html)
    * [Bauble Hunt](games/baublehunt.html)
    * [The Hunger Baubles](games/thehungerbaubles.html)
    * [King of the Bubble](games/kingofthebubble.html)
        * [King of Space (Variant)](games/kingofthebubble.html#kos)
    * [Discovery Quest](games/discoveryquest.html)
* External Resources
    * [Twitch Archive](https://www.twitch.tv/collections/a1gxFZRvzRXe_w) - Recent Tournament Archives
    * [YouTube Playlist](https://www.youtube.com/playlist?list=PL1DMX9HzuNPTiYpd1KslkAAsSY1yMrEgh) - Past Competitions
    * [Beat Senioritis with a Real-Time Networked Space Sim - CSTA 2016](https://www.youtube.com/watch?v=ZUBB8pRRgHI)
    * [You Have Died of Dysentery: Games in Education Are Still Alive - PAXDev 2014](http://www.mikeware.com/2014/08/you-have-died-of-dysentery-games-in-education-are-still-alive/)
    * [Reach for the Stars - PAXDev 2012](http://www.mikeware.com/2012/09/reach-for-the-stars-educating-the-next-generation-using-games/)
* [Development](dev/index.html) - Extend Space Battle Arena

