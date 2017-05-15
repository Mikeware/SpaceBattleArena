---
title: Development
outline-header: Common Development Task Guides
outline:
 - { url: "Build.html", title: "Build Packages" }
 - { url: "AddSubgame.html", title: "Adding a Subgame" }
---

Development
=========
Space Battle Arena is developed in two parts:

* The client is developed in Java.
* The server is developed in Python.

In some cases you can just make modifications to the server without making changes to the client.  However, if you want the full range of capabilities.  You should setup development environments for both.

Development Tools
----------------------
* Visual Studio 2017 Community
* [Eclipse](https://eclipse.org/) or [jGRASP](http://www.jgrasp.org/)

Dependencies
----------------
Space Battle was built against the following versions of libraries:

* Java Client
    * [Gson 2.2](https://github.com/google/gson)
* Python Server
    * [Python 2.7.12](https://www.python.org/downloads/release/python-2712/)
    * [PyMunk 3.0.0](https://pypi.python.org/pypi/pymunk/3.0.0)
    * [PyGame 1.9.1](http://www.pygame.org/download.shtml)
    * [Py2Exe 0.6.9](http://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/) (for server executable build)
* Webpage
    * [See Setup GitHub Pages](SetupGitHubPages.html)
