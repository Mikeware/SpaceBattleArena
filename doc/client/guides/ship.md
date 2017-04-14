---
title: Getting to Know Your Ship
nav:
 - { url: "index.html", title: "Space Battle Academy" }
---

Never give-up, never surrender!
==============

Your Spaceship is your livelihood Cadet!  

Now that you have oriented yourself within the Universe, it's time to learn about telling your ship how to do perform commands.

> Be sure to instruct it well; as after your simulations, it must venture completely on its own.

The Spaceship has three main metrics that you'll want to monitor: 

 - Health
 - Shields
 - Energy
 
Each is a limited resource which can be used, depleted, and charged.  

Of course, when your ship's health is depleted it'll explode spectacularly.  You will be requisitioned a new ship at that time to continue your mission, though it may cost you some points (depending on the current mission scenario).

Shields will help protect your ship's health, but must be engaged pre-emptively before taking damage.

> You ship can be damaged by colliding with other objects in the universe, when hit by enemy fire, or when eaten by a dragon...

Finally, your ship has an energy reserve.  

> **Any action you wish your ship to perform requires energy.**  
 
Your ship's energy will slowly and automatically recharge over time.

Ship Control
============

In order to control your ship, you must issue commands.  Your ship must decide what to do based on the information it is given and whatever you've told it to 'remember'.  Each command may require an initial amount of energy to perform as well as have an ongoing energy cost if the action requires a period of time to perform.  

Some commands must wait for the action to be completed before you can issue the next command; these are called **blocking** commands.  Other commands may start and continue the action while you can issue a new command (*non-blocking* commands).  It will be important for you to understand the differences in these two behaviors when programming your spaceship.

> Every time your ship has 'completed' processing a command (and waiting for it to finish if it was blocking), it will ask you to tell it what to do next.

> This process repeats indefinitely until the mission has ended.

An important thing to note is that your ship's computer can only be concurrently processing up to **four** commands at once.  If you exceed that limit, the oldest command will be 'forgotten'.  This is important when trying to execute multiple non-blocking commands together.

> If your ship does not have the required energy to continue executing a command, your **energy will be depleted** and the command will abort.  If you try to reissue the same command, it is possible to get stuck in a loop where you are constantly draining your ships resources but not doing anything.

Be prudent about tracking energy usage and making sure that you give yourself time to recharge or collect energy after performing large complex maneuvers.
