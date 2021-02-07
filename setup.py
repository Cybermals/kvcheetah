from glob import glob
import os
from setuptools import Extension, setup

from Cython.Build import cythonize

#Load readme file
with open("README.md", "r") as f:
    long_desc = f.read()

#Patch for Windows
import sys

if sys.platform == "win32":
    import distutils.cygwinccompiler
    distutils.cygwinccompiler.get_msvcr = lambda: []

#Run setup
setup(
    long_description = long_desc,
    long_description_content_type = "text/markdown",
    ext_modules = cythonize([
        Extension("kvcheetah.joystick", ["kvcheetah/joystick.py"]),
        Extension("kvcheetah.matrix", ["kvcheetah/matrix.pyx"]),
        Extension("kvcheetah.sprite", ["kvcheetah/sprite.py"]),
        Extension("kvcheetah.tilemap", ["kvcheetah/tilemap.py"]),
        Extension("kvcheetah.vector", ["kvcheetah/vector.pyx"])
    ])
)
