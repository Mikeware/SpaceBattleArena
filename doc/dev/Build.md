---
title: Building Space Battle Arena
nav:
 - { url: "index.html", title: "Development" }
---

Building Space Battle Arena
=====================

This document will explain how to build the client and server Space Battle Arena packages.

Dependencies
------------
Make sure you have downloaded and installed all the Python Server dependencies listed on the [Development Guide Home](index.html).

Download the [gson-2.2.jar]({{ site.releasepath }}/gson-2.2.jar) and place it in the root of your downloaded copy of Space Battle Arena [repository](https://github.com/Mikeware/SpaceBattleArena.git).

Building
--------
Make sure **javac**, **javadoc**, and **python** are part of your environment path.  Open up a command window at the root of the repository and type 'compile'.

If all is successful, a 'bin' directory should appear and contain a SpaceBattle.jar file and a SBAServer.zip file.

Updated java docs will be copied to doc/client/java_doc.

For info on building the website see [Setup GitHub Pages](SetupGitHubPages.html).
