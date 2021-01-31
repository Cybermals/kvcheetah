# kvcheetah
A lightweight 2D game engine based on Kivy.


Installation Instructions (pip)
-------------------------------
1. on Windows, execute ```pip install kvcheetah```
   on Linux, execute ```sudo pip3 install kvcheetah```
2. to test your installation on Windows, execute ```python -m kvcheetah```
   on Linux, execute ```python3 -m kvcheetah```


Installation Instructions (GitHub)
----------------------------------
1. download the latest wheel from the release section that matches your OS
2. open a terminal or command prompt window and use pip to install the downloaded
wheel file
3. to test your installation on Windows, execute ```python -m kvcheetah```
   on Linux, execute ```python3 -m kvcheetah```


Building Instructions
---------------------
1. clone this repo
2. open a terminal or command prompt window and switch to the "kvcheetah" folder
3. on Windows, execute ```python setup.py bdist_wheel```
   on Linux, execute ```python3 setup.py bdist_wheel```


Features
--------
* sprites
    * hardware-accelerated
    * supports basic collision detection
    * supports rotation
    * supports color adjustment

* tilemaps
    * hardware-accelerated
    * supports adjustable viewport
    * supports scrolling
    * implements viewport culling
    * supports collision detection


Tested On
---------
* Python 3.6.8 and Kivy 1.11.0 for Windows Vista (32-bit)
* Python 3.8.5 and Kivy 2.0.0 for Lubuntu 20.04 (64-bit)
* MacOS X
* Android 10 (experimental)


Status
------
![Build MacOS Wheels](https://github.com/Cybermals/kvcheetah/workflows/Build%20MacOS%20Wheels/badge.svg?branch=main)
![Build Ubuntu Wheels](https://github.com/Cybermals/kvcheetah/workflows/Build%20Ubuntu%20Wheels/badge.svg?branch=main)
![Build Windows Wheels](https://github.com/Cybermals/kvcheetah/workflows/Build%20Windows%20Wheels/badge.svg?branch=main)
![Build Source Package](https://github.com/Cybermals/kvcheetah/workflows/Build%20Source%20Package/badge.svg?branch=main)
