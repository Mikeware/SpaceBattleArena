# Installing on Mac OS X

1. Install Xcode command line tools
```
$ xcode-select --install
```

2. Install Homebrew (aka brew) 
```
$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
$ brew install caskroom/cask/brew-cask
```

3. Install libraries needed for pygame using brew 
```
$ brew cask install xquartz
$ brew install python
$ brew linkapps python
$ brew install mercurial
$ brew install sdl sdl_image sdl_ttf portmidi libogg libvorbis
$ brew install sdl_mixer --with-libvorbis
```

4. Install SpaceBattleArena requirements using pip
```
$ pip install -r requirements.txt
```

5. Start SpaceBattleArena
```
$ python SBA_Serv.py
```
