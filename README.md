# MATE-2023

## Installation
- Install virtualenv https://virtualenv.pypa.io/en/latest/installation.html
- `virtualenv env` to create the virtual environment
- Run `source env/bin/activate` to start the virtual environment
- Run `pip install -r requirements.txt` to install project dependencies
- Run `deactivate` when you are done


## Cameras
In order for the driver station GUI to properly access rover cameras:
- create a file in the root project directory called "cams.txt"
- find the device numbers of the cameras you want to use
- place the numbers in order separated by newline in "cams.txt"
    - example, say you wish to use cameras 6, 5, 8, 10
    - You would place "6\n5\n8\n10" into cams.txt
