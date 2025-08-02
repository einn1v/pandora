# Pandora v1.0.0

## About
Pandora is a CLI based password manager made for safe and efficient password management.

## Installation

Make sure you have [python](https://www.python.org/ftp/python/3.13.5/python-3.13.5-amd64.exe) installed.

### Windows

- Open up a cmd or powershell window, make sure you've navigated to a folder where you want to place/download the application

- Clone the Github repository with the following command:

```sh
git clone https://github.com/einn1v/pandora.git
```

- Enter pandora's folder you've just installed:

```sh
cd pandora
```

- Install the required dependencies:

```sh
pip install -r requirements.txt
```

- Enable commands before initializing them:

```sh
pip install -e .
```

- Run the ``setup.py`` file to initialize the user commands:

```sh
python setup.py
```

Congrats!
You've just installed pandora, you can now use the commands ``pandora``, ``pdr`` to start the program.

### Linux

- Open up the terminal, make sure you've navigated to a folder where you want to place/download the application

- Clone the Github repository with the following command:

```sh
git clone https://github.com/einn1v/pandora.git
```

- Enter pandora's folder you've just installed:

```sh
cd pandora
```

- Install the required dependencies:

```sh
pip install -r requirements.txt
```

- Run the ``setup.py`` file to initialize the main script to the ``~/`` or ``user`` directory:

```sh
python setup.py
```

- Navigate to the user directory (This is the default path your terminal opens, the pandora file will be initialized here for easier access)

```sh
cd ~
```

Congrats!
You've just installed pandora on linux, you can now use pandora by opening a terminal and typing ``python pdr.py``

### Note
I've documented various parts of the code with comment lines, feel free to learn from this script.
The commands ``pdr``and ``pandora`` aren't working on linux yet due to some distributions preventing 2 of the installation steps, I plan to fix this in a later version.
