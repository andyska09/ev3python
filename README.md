# ev3python
Playground to get started with python programming on LEGO EV3 and Windows 10.

## Setting up development environment

### Install ev3dev image on the brick
Follow steps on:

    http://www.ev3dev.org/docs/getting-started/

#### Connect PC with the brick
There are 3 options, described on:

    http://www.ev3dev.org/docs/networking/

- **wifi** - I use Edimax EW-7811Un 802.11n Wireless Adapter, officially supported by LEGO’s software. 
I set the following values on the brick:

            Wireless and Networking | Wi-Fi 
                Powered: on
            Wireless and Networking | Wi-Fi | <my-network-name> | Network Connection | IPv4
                IP:      10.0.0.6
                MASK:    255.255.255.0
                GATEWAY: 10.0.0.138
    When connected, test it from command line:

        > ping ev3dev
        Pinging ev3dev [10.0.0.6] with 32 bytes of data:
        Reply from 10.0.0.6: bytes=32 time=14ms TTL=64
        Reply from 10.0.0.6: bytes=32 time=11ms TTL=64
        Reply from 10.0.0.6: bytes=32 time=11ms TTL=64
        Reply from 10.0.0.6: bytes=32 time=32ms TTL=64

        Ping statistics for 10.0.0.6:
            Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
        Approximate round trip times in milli-seconds:
            Minimum = 11ms, Maximum = 32ms, Average = 17ms

- wired by USB - worked, but it is rather unconfortable 
- bluetooth - did not work for me

### Install Git for Windows
While not necessary for python programming for ev3, it allows to get and backup sources. Download installer from:

    https://git-for-windows.github.io/

### Install GOW 
GOW is a set of Unix command line utilities for Windows. I use ssh from command line to connect to the brick and to start .py programs.

    https://github.com/bmatzelle/gow

Alternative is to install PuTTY, an SSH client for Windows.

### Install Visual Studio Code
It is a free modern editor for programmers.

#### Add ftp-sync extension   
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

## Getting Started

### Get sources of this project
Switch to your folder with projects and clone the project. Switch to the ev3dev project.

    > cd workspace 
    > git clone https://github.com/andyska09/ev3python.git
    > cd ev3python

### Open editor with project
Run VS Code. 
Open menu File | Open Folder ... | select ev3dev 

### Init ftp-sync extension for the project   
- press Ctrl+Shift+P and type

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

#### Add Python extension
An extension with rich support for the Python language (including Python 3.6), with features like auto indenting, intellisense, code formatting.

### Run the sample
Python files shall already be on the brick, copied by sftp extension of editor. Login to the brick. Verify that python files are on the brick. Make _text-to-speach.py_ executable and execute it. It shall say _LEGO Mindstorms EV3 is awesome and with  ev3dev is super awesome_.

    > ssh robot@ev3dev -pw maker 
    $ ls
    motor.py  text-to-speach.py  ...
    $ chmod +x text-to-speach.py   
    $ ./text-to-speach.py 

## Create your programs
Follow the guide _learn_ev3_python_ to get into ev3python. Samples in this project are taken from it:
    
    https://sites.google.com/site/ev3python/learn_ev3_python/basics-1

### Three important prerequisites to get python file executable
One can start python program like below. 
 
    $ ./text-to-speach.py 

To achieve it, the following shall be done. 

- Put the line to the beginning of the .py file

        #!/usr/bin/env python3

- Set End of Line sequence to **LF** (not CRLF) for python files in the VS Code footer in bottom right.

- Make program executable on the brick

        $ chmod +x text-to-speach.py  


## Alternative way to start python programs on the brick

    > ssh robot@ev3dev -pw maker "python3 text-to-speach.py"

    > plink -ssh robot@ev3dev -pw maker "python3 text-to-speach.py"

### Configure Default Build Task
Above command can become Default Build Task, executed by Ctrl + Shift + B. Drawback is that it takes cca 10s to start the program, while starting from ssh session (e.g. in PUTTY) takes cca 3sec.

Below is .vscode/tasks.json

    {
        // See https://go.microsoft.com/fwlink/?LinkId=733558
        // for the documentation about the tasks.json format
        "version": "2.0.0",
        "tasks": [
            {
                "taskName": "Run .py on EV3",
                "type": "shell",
                "command": "ssh robot@ev3dev -pw maker 'python3 ${fileBasename}'",
                "group": {
                    "kind": "build",
                    "isDefault": true
                },
                "presentation": {
                    "reveal": "always",
                    "panel": "shared"
                }
            }
        ]
    }




