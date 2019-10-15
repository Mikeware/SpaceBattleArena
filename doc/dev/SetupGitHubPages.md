---
title: Setup GitHub Pages
nav:
 - { url: "index.html", title: "Development" }
---

Installing [Wyam](https://wyam.io/) Doc Builder
-------------------------

1. Install Wyam on the command line with `dotnet` (requires [.NET Core](https://dotnet.microsoft.com/download)):

	```
	dotnet tool install -g Wyam.Tool
	```

2. Restart command line (or VS Code)
3. Doc system assumes another copy of repo to `gh-pages` branches has been checked out alongside the repo in a `gh-pages` directory.
4. Type `wyam` to build, **clear all non-.git folders in gh-pages folder before-hand if making significant structure changes.**
5. To preview the site and watch for changes use:

	```
	wyam -p -w --virtual-dir "/SpaceBattleArena"
	```
6. Open your browser to [http://localhost:5080/SpaceBattleArena/](http://localhost:5080/SpaceBattleArena/) (notice the ending slash).
7. Make 2 branches one off `master` and one off `gh-pages` in order to submit two PRs for updates to source docs and generated output.
