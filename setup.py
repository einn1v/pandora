import os
import shutil
from setuptools import setup
from setuptools.command.install import install

class Install(install):
    def run(self):
        install.run(self)

        path = os.path.expanduser("~/.local/share")
        directory = os.path.join(path, "Pandora")
        
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        src = os.path.join(os.path.dirname(__file__), "main.py")
        dst = os.path.join(directory, "main.py")

        if not os.path.exists(dst):
            shutil.copy(src, dst)
            print("Pandora installed successfully.")
        else:
            print("Pandora is already installed.")

with open(os.path.dirname(__file__), "requirements.txt") as file:
    reqs = file.read().splitlines()

setup(
    name="pandora",
    description="Pandora is a CLI password manager for safe and efficient password management.",
    version="1.0.0",
    packages=[],
    install_requires=reqs,
    cmdclass={
        "install": Install,
        "init": Install,
        "-i": Install,
    },
    entry_points={
        "console_scripts": [
            "pandora = main:main",
            "pdr = main:main",
        ]
    }
)
