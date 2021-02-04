from setuptools import Extension, setup
from Cython.Build import cythonize

#Load readme file
with open("README.md", "r") as f:
    long_desc = f.read()

#Run setup
setup(
    long_description = long_desc,
    long_description_content_type = "text/markdown",
    ext_modules = cythonize([
        Extension("joystick", ["kvcheetah/joystick.py"]),
        Extension("sprite", ["kvcheetah/sprite.py"]),
        Extension("tilemap", ["kvcheetah/tilemap.py"])
    ])
)