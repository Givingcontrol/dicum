# Dicum

Dicum is a small game for tease and denial lovers, that like to get locked up. 

![Game Preview](https://github.com/joka-beep/dicum/blob/master/preview/preview-alpha.png)

## How does it work?

You get a set of buttons that allow you to activate the next action, like roulette, you don't know what will be your next draw. Possible actions are 

* Draw a closed lock
* Draw an open lock
* Draw a teaser-image
* Draw a website (possibly a teaser)
* Draw a time that is added to your next lockup time

If you draw more than the limit of closed locks (currently 2), the game will stop and is blocked for the lockup time. The lockup time is at minimum one hour and might be increased when you draw a time increase.

If you draw open locks, you get released and can do whatever you want until you start to play the game again.

## Installation

The installation is only possible on linux system at the moment and is not streamlined, yet. 

If you want to try the game, I might provide you with a test .zip file, however, image copyrights are not checked. In case of any trouble, send me a message on github or email me.

* Clone the repository
* Create a virtual environment for python
* Source the environment
* Install requirements from requirements.txt

In order to run the game create a folder to store the game state
```
$ sudo mkdir /var/lib/dicum/
```

Install fonts:
```
$ rsync -a ../dicum/fonts/ ~/.fonts
```

Create a csv file that holds all possible actions:
```
$ cd /path/to/game/dicum
$ touch /resources/actions.csv
```

possible content: 
```
img,pic1.png,0
img,pic2.png,0
img,pic3.png,0
num,2,0
num,3,0
num,5,0
num,5,0
num,12,0
lock,unlock,0
lock,unlock,0
lock,lock,0
lock,lock,0
```
img : image name
num : number of hours added to your lockup time
lock: lock/unlock is a closed, open lock, respectively

the last number (0) shall be used in the future, but is not used for now.

The images (img,pic1.png,0) must exist in `dicum/resources/images/`. Since, I have not checked any image copyrights, you'll have to add your own teaser images to the following dir:
```
/path/to/game/dicum/resources/images/
```

when you sourced your environment, run the game using
```
$ python DicumUI/DicumUI.py recourses/actions.csv
```
