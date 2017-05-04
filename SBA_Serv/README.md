Installing on Mac OS X
======================

See [video walkthrough](https://www.youtube.com/watch?v=sGbfHNEpwm4) to follow along.  Thanks to Brian Fleischman for video and Derrick McMillen for initial instructions.

1. Open a command line to the location you'd like to install [Space Battle](http://mikeware.github.io/SpaceBattleArena/).

2. Clone the repository, this should create a new '**SpaceBattleArena**' folder.
```
git clone https://github.com/Mikeware/SpaceBattleArena.git
```

3. Navigate to the Server Directory *SBA_Serv*
```
cd SpaceBattleArena
cd SBA_Serv
```

4. Install Xcode command line tools
```
xcode-select --install
```

5. Install [Homebrew](https://caskroom.github.io/) (aka brew) 
```
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

6. Install libraries needed for pygame using brew 
```
brew cask install xquartz
brew install python
brew linkapps python
brew install mercurial
brew install sdl sdl_image sdl_ttf portmidi libogg libvorbis
brew install sdl_mixer --with-libvorbis
```

7. Install SpaceBattleArena requirements using pip
```
pip install -r requirements.txt
```

8. Start SpaceBattleArena
```
python SBA_Serv.py
```

Find more information about [configuring](http://mikeware.github.io/SpaceBattleArena/server/config.html) and [running](http://mikeware.github.io/SpaceBattleArena/server/usage.html) the server on the main site.

Just add configuration files to the end of the 'python SBA_Serv.py' command instead of the 'SBA_Serv' shown in the examples.
