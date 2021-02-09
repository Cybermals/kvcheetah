import sys
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

#Define extensions
extensions = [
    Extension("kvcheetah.math.matrix", ["kvcheetah/math/matrix.pyx"]),
    Extension("kvcheetah.math.vector", ["kvcheetah/math/vector.pyx"]),
    Extension("kvcheetah.graphics.sprite", ["kvcheetah/graphics/sprite.py"]),
    Extension("kvcheetah.graphics.tilemap", ["kvcheetah/graphics/tilemap.py"]),
    Extension("kvcheetah.uix.joystick", ["kvcheetah/uix/joystick.py"])
]

#Run setup
setup(
    long_description = long_desc,
    long_description_content_type = "text/markdown",
    ext_modules = cythonize(extensions)
)
