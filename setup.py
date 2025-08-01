from setuptools import setup

with open("requirements.txt") as file:
    reqs = file.read().splitlines()

setup(
    name="pandora",
    description="Pandora is a CLI password manager for safe and efficient password management.",
    version="1.0.0",
    py_modules=["main"],
    install_requires=reqs,
    entry_points={
        "console_scripts": [
            "pandora = main:main",
            "pdr = main:main",
        ]
    }
)
