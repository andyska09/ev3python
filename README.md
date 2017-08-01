# ev3python
Playground to get started with python programming on LEGO EV3 and Windows 10

> git clone https://github.com/andyska09/ev3python.git
## Setting up development environment
### Install ev3dev image on the brick
- follow steps on http://www.ev3dev.org/docs/getting-started/
- use wired connection via USB  

### Install Visual Studio Code

#### Add ftp-sync extension   
https://marketplace.visualstudio.com/items?itemName=lukasz-wronski.ftp-sync

It allows to upload python files to the brick whenever file is saved.

- open command line Ctrl+P and execute
    > ext install ftp-sync
- initialize it by Ctrl+Shift+P and type
    > Ftp-sync: Init
- set values in .vscode/ftp-sync.json as below

        {
            "remotePath": "./",
            "host": "ev3dev",
            "username": "robot",
            "password": "maker",
            "port": 22,
            "secure": true,
            "protocol": "sftp",
            "uploadOnSave": true,
            "passive": false,
            "debug": false,
            "privateKeyPath": null,
            "passphrase": null,
            "ignore": [
                "\\.vscode",
                "\\.git",
                "\\README.md"
            ],
            "generatedFiles": {
                "uploadOnSave": false,
                "extensionsToInclude": [],
                "path": ""
            }
        }

## Create your sample program
Put the following lines to the beginning of the .py file

    #!/usr/bin/env python3
    # from ev3dev.ev3 import *

Set End of Line sequence LF (not CRLF) for python files in the VS Code footer in bottom right. It allows to make python file executable.

Save the file.
It will be transfered to the brick. 

## Execute your program

- Connect to the brick by ssh in integrated terminal of VS Code.

        $ ssh robot@ev3dev
        password: maker

        $ ls
        motor.py  text-to-speach.py  x.py

- Make program executable

        $ chmod +x text-to-speach.py    

- Run the program

        $ ./text-to-speach.py




