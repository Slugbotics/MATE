# MATE

## Git Standards
When making changes to the codebase, use feature branches. Tutorial can be found here https://medium.com/@stephencweiss/a-beginners-guide-to-feature-branch-workflows-with-git-7ae442df8e11

Donts:
- Do not push directly onto main, make a branch, make a pr, squash and merge.
- Do not let branches sit for too long, if they arent merged within a week or two, discard it and move on.
- Do not make changes to the build system without adding them to this README
- Do not add dependencies without adding them to requirements.txt

Dos:
- Use feature branches, make pull requests, squash and merge
- Keep branches to one feature at most
- Use interactive rebase as the default merge strategy
- Format your code using clang-format (c++) or black (python)

Python Standards:
- Use type declarations / hints for all functions
- write docstrings for non-obvious functiions / methods
- always write docstrings for classes
- keep commenting minimal, if you code is not obvious, it is probably too complicated
- keep nesting minimal, if you can nest less, you probably should

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
