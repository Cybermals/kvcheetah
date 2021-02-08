from glob import glob
import os
import sys
from setuptools import Extension, setup

from Cython.Build import cythonize

library_dirs = []

if sys.platform == "win32":
    #On Windows we must make sure that SDL2 is on the DLL search path
    from kivy_deps.sdl2 import dep_bins
    library_dirs.extend(dep_bins)

#Load readme file
with open("README.md", "r") as f:
    long_desc = f.read()

#Patch for Windows
import sys

if sys.platform == "win32":
    import distutils.cygwinccompiler
    distutils.cygwinccompiler.get_msvcr = lambda: []

#Define extensions
extensions = [
    Extension("kvcheetah.math.matrix", ["kvcheetah/math/matrix.pyx"]),
    Extension("kvcheetah.math.vector", ["kvcheetah/math/vector.pyx"]),
    Extension("kvcheetah.graphics.opengl._gl", 
        ["kvcheetah/graphics/opengl/_gl.pyx"]),
    Extension("kvcheetah.graphics.opengl._gl_sdl2", 
        ["kvcheetah/graphics/opengl/_gl_sdl2.pyx"], libraries = ["SDL2"], 
        library_dirs = library_dirs),
    Extension("kvcheetah.graphics.sprite", ["kvcheetah/graphics/sprite.py"]),
    Extension("kvcheetah.graphics.tilemap", ["kvcheetah/graphics/tilemap.py"]),
    Extension("kvcheetah.uix.joystick", ["kvcheetah/uix/joystick.py"])
]

if sys.platform != "win32":
    extensions.extend(
        [
            Extension("kvcheetah.graphics.opengl._gl_glx", 
                ["kvcheetah/graphics/opengl/_gl_glx.pyx"], libraries = ["GLX"])
        ]
    )

#Run setup
setup(
    long_description = long_desc,
    long_description_content_type = "text/markdown",
    ext_modules = cythonize(extensions)
)
