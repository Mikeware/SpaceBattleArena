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
3. Type `wyam` to build.
4. Use `wyam -p -w --virtual-dir "/SpaceBattleArena"` to preview the site and watch for changes.
