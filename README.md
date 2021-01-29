# kvcheetah
A lightweight 2D game engine based on Kivy.


Installation Instructions
-------------------------
1. download the latest wheel from the release section
2. open a terminal or command prompt window and use pip to install the downloaded
wheel file
3. to test your installation, execute ```python -m kvcheetah```; if that fails,
try executing ```python3 -m kvcheetah``` instead


Building Instructions
---------------------
1. clone this repo
2. open a terminal or command prompt window and switch to the "kvcheetah" folder
3. run ```python setup.py bdist_wheel```; if that filas, try running
```python3 setup.py bdist_wheel``` instead


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


Tested On
---------
* Python 3.8.5 and Kivy 2.0.0 for Lubuntu 20.04 (64-bit)
* Python 3.6.8 and Kivy 1.11.0 for Windows Vista (32-bit)
