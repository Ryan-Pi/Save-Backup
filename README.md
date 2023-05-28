# Save-Backup

## Summary

Python CLI script built to backup local files from one folder to another folder, and to restore backups to specified save locations. File locations are saved in a json file, which stores a json object that contains the name of a file location, the location of the files (save path) and where the files should be backed up to. Files in the save location will be saved in a folder at the specified backup path in a name-yy-mm-dd format by default.

Primarily built as a way to practice Python and to learn more about some common modules used in python as well as file i/o operations, json module and the use of the argparse module.

## Commands

usage: save_backup.py [-h] [-l] [name] {add,change,save,load,remove} ...

Script to backup save games to another location

positional arguments:
  name                  name of game to be saved

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            list all saved game paths

subcommands:
  {add,change,save,load,remove}
                        add, change, save, load
    add                 add new game paths
    change              change existing game paths
    save                backup save game
    load                restore backup to save games
    remove              remove game path

### Subcommand Arguments
#### Add
save_backup.py [-h] [-l] [name] add [savepath] [backup]
positional arguments: 
savepath : save path for game/files
backup : backup path for game/files
#### Change
optional arguments:
-cn, --changename : change name of invoked game to this
-sp, --savepath : change save path of invoked game to this
-bp, --backup : change backup path of invoked game to this

#### Save
optional arguments:
-t, --title : specify what the backup folder should be called instead of the default game-yy-mm-dd format

#### Load
optional arguments:
-db, --deletebackup : flag to delete backup after restoring it to save location
-do, --deleteold : flag to delete all backups other than the most recent after restoring specified backup to save location

#### Remove
optional arguments:
-f, --files : flag to delete all backups for the specified game from backup directory

 
