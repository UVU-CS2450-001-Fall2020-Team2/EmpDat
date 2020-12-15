# EmpDat
Is this hard to read? [View this on GitHub!](https://uvu-cs2450-001-fall2020-team2.github.io/EmpDat/)

Employee Database Application for CS 2450-001 Fall 2020.
- Kevin Thorne
- Tanner Olsen
- Kim Soto
- Luke Barrett
- Caleb Probst
- Colton Robbins
- Joshua Ley

Licenses and attributions attached in the LICENSES.txt and
    under Help>About in the application

## Installing

EmpDat was designed with Windows users in mind. 
However, EmpDat can be run on any operating system Python is supported on.

### The easy way

##### Windows:
1. Unzip the `Portable.win.zip` to a location of choice.
2. Run `EmpDat.exe`
3. Done!

#### The harder way: from included environment
Most of the steps require a terminal window.
1. Acquire the source with dependencies from the deployment ZIP archive
    - `src_w_deps.zip`
2. Ensure Python 3 (version 3.6 minimum) is installed.
3. Activate the virtual environment by running:
    - `.\venv\Scripts\activate.bat`
4. Install dependencies: `pip install -r requirements.txt`
5. Run `python EmpDat.py`

#### The hard way: from scratch
Most of the steps require a terminal window.
1. Acquire the source from the deployment ZIP archive
    - `src.zip`
2. Ensure Python 3 (version 3.6 minimum) is installed.
3. Install dependencies: `pip3 install -r requirements.txt`
4. Run `python3 EmpDat.py`


## First Run
1. Login as the super-admin:
    - Employee ID: `-1`
    - Password: `Ineed2changemypassword!`
2. On the top bar, click **File > Change Password** 
    and change the super-admin's password to preference
3. If desired, import previous database of employees
    - On the top bar, click **Import > Employees** and locate the previous CSV database
    - *Note: the database can be converted back into a CSV using the Employee Directory Report*
4. Consult the User Manual for performing other operations

## Development

### Environment Setup
A virtual environment (a shadow copy of an already installed Python) is recommended Python

1. In the folder of choice: `git clone https://github.com/UVU-CS2450-001-Fall2020-Team2/EmpDat.git`
2. Run `python3 -m venv venv/`
3. Activate the virtual environment
    - Windows: `venv/Scripts/activate.bat`
    - Linux/Unix/Mac: `source venv/bin/activate`
4. Install dependencies: `pip3 install -r requirements.txt`
5. Run `python EmpDat.py`

Any time anything needs to be ran or installed 
    within the application, activate the virtual environment using
    Step 3 above. Deactivation can be done with the command `deactivate`.

### Documentation
##### [ui/](ui/index.html) - Front end
##### [tests/](tests/index.html) - Tests
##### [lib/](lib/index.html) - Back end
##### [EmpDat.py](EmpDat.html) - Main