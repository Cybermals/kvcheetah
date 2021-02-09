from pythonforandroid.recipe import CythonRecipe
from pythonforandroid.toolchain import Recipe, shprint, current_directory
from os.path import basename, exists, join
import sh
import glob


class KvCheetah(CythonRecipe):
    # This could also inherit from PythonRecipe etc. if you want to
    # use their pre-written build processes

    name = "kvcheetah"
    version = "2.0.1"
    url = "https://github.com/Cybermals/kvcheetah/archive/v{version}.tar.gz"
    # {version} will be replaced with self.version when downloading

    depends = ["python3", "kivy", "cython"]  # A list of any other recipe names
                                             # that must be built before this
                                             # one

    conflicts = []  # A list of any recipe names that cannot be built
                    # alongside this one

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        # Manipulate the env here if you want
        return env

    def should_build(self, arch):
        # Add a check for whether the recipe is already built if you
        # want, and return False if it is.
        return True

    def prebuild_arch(self, arch):
        super().prebuild_arch(arch)

        # Do any extra prebuilding you want, e.g.:
        #self.apply_patch("path/to/patch.patch")

    def build_arch(self, arch):
        super().build_arch(arch)

        # Build the code. Make sure to use the right build dir, e.g.
        #with current_directory(self.get_build_dir(arch.arch)):
        #    sh.ls("-lathr")  # Or run some commands that actually do
                              # something

    def postbuild_arch(self, arch):
        super().prebuild_arch(arch)

        # Do anything you want after the build, e.g. deleting
        # unnecessary files such as documentation

    def cythonize_build(self, env, build_dir = "."):
        super(KvCheetah, self).cythonize_build(env, build_dir = build_dir)

    def cythonize_file(self, env, build_dir, filename):
        #Ignore any file in the following list
        do_not_cythonize = []

        if basename(filename) in do_not_cythonize:
            return

        #Cythonize the file
        super(KvCheetah, self).cythonize_file(env, build_dir, filename)


recipe = KvCheetah()
