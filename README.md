# Chess tournament management - Swiss system

## Menu

* [Overview](#overview)
* [Program setup](#program-setup)
	- [Overview](#creation-of-a-virtual-environment)
* [Program execution](#program-execution)
* [Flake8](#flake8)
* [Screenshot](#screenshot)
	- [Tournament menu](#tournament-menu)
	- [Reports](#reports)

## Overview

About this program :
- it allows to manage chess tournaments according to the Swiss system
- it allows to manage the rating of registered players 
- it allows to display different reports
- it uses a json database to store tournaments and players

![Screenshot of menu](https://github.com/Prud-homme/image-data-bank/blob/main/projet_4/menu.gif?raw=true)

[Link to screenshot](#screenshot)

## Program setup

### Creation of a virtual environment

**On Windows**
```
$ python3 -m venv c:\path\to\myenv
$ myenv\Scripts\activate.bat
```

**On Unix or MacOS**
```
$ python3 -m venv /path/to/myenv
$ source myenv/bin/activate
```

**To install packages from the requirements.txt file**
```
(myenv) $ pip3 install -r requirements.txt
```

**To disable the virtual environment, run:**
```
(myenv) $ deactivate
```

## Program execution
When the virtual environment is activated and you are placed in the folder where the main file is located, launch the program with the command:
```
(windows-env) $ python main.py
```
```
(unix-mac-env) $ python3 main.py
```

In order to get more information during the execution of the program you can run the command:
```
(windows-env) $ python main.py --loglevel INFO
```
```
(unix-mac-env) $ python3 main.py --loglevel INFO
```
## Flake8
The .flake8 file allows to configure flake8 and thus it will be enough to launch the `flake8` command to generate the report
## Screenshot
ℹ️ Use Ctrl + Click for open in new tab
### Tournament menu
[Create a tournament](https://github.com/Prud-homme/image-data-bank/blob/main/projet_4/tournament-menu/create.png?raw=true)

[Load a tournament](https://github.com/Prud-homme/image-data-bank/blob/main/projet_4/tournament-menu/load.png?raw=true)

[Add a player to the tournament](https://github.com/Prud-homme/image-data-bank/blob/main/projet_4/tournament-menu/addplayer.png?raw=true)

[Create a player](https://github.com/Prud-homme/image-data-bank/blob/main/projet_4/tournament-menu/createplayer.png?raw=true)

[Load a player](https://github.com/Prud-homme/image-data-bank/blob/main/projet_4/tournament-menu/loadplayer.png?raw=true)

[Resume menu for a tournament in progress](https://github.com/Prud-homme/image-data-bank/blob/main/projet_4/tournament-menu/tournamentresume.png?raw=true)

[See the tournament information](https://github.com/Prud-homme/image-data-bank/blob/main/projet_4/tournament-menu/tournamentinfo.png?raw=true)

[Display of matches generated for the round](https://github.com/Prud-homme/image-data-bank/blob/main/projet_4/tournament-menu/generation.png?raw=true)

[Display current matches](https://github.com/Prud-homme/image-data-bank/blob/main/projet_4/tournament-menu/displaycurrent.png?raw=true)

[Complete a match](https://github.com/Prud-homme/image-data-bank/blob/main/projet_4/tournament-menu/completematch.png?raw=true)

[Complete a turn](https://github.com/Prud-homme/image-data-bank/blob/main/projet_4/tournament-menu/completeturn.png?raw=true)

### Reports
[List all players by alph](https://github.com/Prud-homme/image-data-bank/blob/main/projet_4/tournament-menu/playeralphabetic.png?raw=true)

[List all tournaments](https://github.com/Prud-homme/image-data-bank/blob/main/projet_4/tournament-menu/listtournaments.png?raw=true)

[Selecting a tournament to access these reports](https://github.com/Prud-homme/image-data-bank/blob/main/projet_4/tournament-menu/abouttournament.png?raw=true)

[Report menu for a tournament selected](https://github.com/Prud-homme/image-data-bank/blob/main/projet_4/tournament-menu/abouttournamentmenu.png?raw=true)

[Final ranking](https://github.com/Prud-homme/image-data-bank/blob/main/projet_4/tournament-menu/abouttournamentfinalranking.png?raw=true)

[List of matches](https://github.com/Prud-homme/image-data-bank/blob/main/projet_4/tournament-menu/abouttournamentmatches.png?raw=true)

[List of rounds](https://github.com/Prud-homme/image-data-bank/blob/main/projet_4/tournament-menu/abouttournamentturn.png?raw=true)

[Filtering player](https://github.com/Prud-homme/image-data-bank/blob/main/projet_4/tournament-menu/filterplayer.png?raw=true)


