# import os to check file size
# import sys to exit script
# import shutil to copy and rm files
# import argparse for parser
# import datetime for naming backups
# import json for saving game entries
import os
import sys
import shutil
import argparse
from datetime import datetime
import json

# python script with json file that saves game paths

JSON_NAME = "games.json"
JSON_PATH = os.getcwd() + "\\" + JSON_NAME

#TODO move save path and backup path out of main()

def main():
    
    global game
    global save_path
    global backup_path
    global locations
    global empty
    locations = []
    #check if json file exists and create if it doesnt
    #open json file containing game save paths
    if(os.path.exists(JSON_PATH)!=True):
        #creates game.json if it doesn't exist
        open(JSON_PATH, "x")
        print("games.json not found, creating a new file!")
    with open(JSON_NAME) as file:
        if(os.stat(JSON_PATH).st_size == 0): 
            #no json
            empty = True
            print("No existing game paths set up!")
            file.close()
        else:
        # load json file
            empty = False
            locations = json.load(file)
            file.close()
    args = parse_args()
    game = args.name
    if args.subcommand == 'add':
        save_path = args.savepath
        backup_path = args.backup
        add()
    elif args.subcommand == 'change':
        if(args.changename != None or args.savepath != None or args.backup != None):
            change(args.changename, args.savepath, args.backup)
        else:
            sys.exit("No change specified! Exiting...")
    elif args.subcommand == 'save':
        save()
    elif args.subcommand == 'load':
        load(args.deletebackup, args.deleteold)
    elif args.subcommand == 'remove':
        remove(args.files)
    if(args.list):
        list()
    # path to find saves
    # path to backup saves
    # command to list games, with path settings saved?
    # command to add games with path settings
    # create folder in specified backup directory, with saves, named date + time
    
    

def add():
    #use Tuple to save game name, save path, backup path?
    #need to check for duplicate game names!
    if '-' in game:
        sys.exit("- is not an allowed character for game names! Exiting...")
    if(next((item for item in locations if item["game"] == game), False)):
        sys.exit(f'{game} already exists!')
    #check paths are valid
    if (os.path.exists(save_path)==False):
        sys.exit("Save path not valid! Exiting...")
    elif(os.path.exists(backup_path)==False):
        sys.exit("Backup path not valid! Exiting...")
    else:
        print("All paths valid!")
    new_json = {
        "game": game,
        "savePath": save_path,
        "backupPath": backup_path
    }
    locations.append(new_json)
    write()
    print(f'{game} added successfully!')

def change(name, save, back):
    #add flag to move previous backups to new directory
    # remove old one, add new one
    # python makes shallow copies, so modifying location
    # will change the dict in locations list
    location = locate()
    if(location == False):
        #exit if no such game has been saved 
        sys.exit(f'{game} has not been added!')
    # optional path
    if(name != None):
        newName = locate(name)
        if(newName == False):
            #checks if an entry for the proposed name change already exists
            if("-" in name):
                print("- is not an allowed character for game names! Name has not been changed")
            else:
                location["game"] = name
        else:
            sys.exit(f'{name} has already been configured with save path {newName["savePath"]} and backup path {newName["backupPath"]}')
    if(save != None):
        if(os.path.exists(save)==False):
            # exit if save path is not valid
            sys.exit("save path not valid")
        location["savePath"] = save
    if(back != None):
        if(os.path.exists(back)==False):
            # exit if backup path is not valid
            sys.exit("backup path not valid")
        location["backupPath"] = back
    # optional backup change
    #check that at least one is being changed
    write()
    print("Change complete!")
    
def remove(delFiles):
    #remove an entry
    location = locate()
    if(location == False):
        sys.exit(f'{game} entry does not exist!')
    locations.remove(location)
    write()
    print(f'Removed entry for {game} with save path {location["savePath"]} and backup path {location["backupPath"]}')
    #add option to delete all back ups for a game
    if(delFiles==True):
        #delete all backup files for game name
        confirm = input(f'Confirm that all backups for {game} should be deleted (y/n)?')
        if(confirm.lower()=='y'):
            shutil.rmtree(location["backupPath"])
            print(f'Removed all files for {game} from {location["backupPath"]}')
        else:
            sys.exit("Removal of backup files aborted!")
    else:
        print(f'Please note that backup files have not been deleted and are stored at {location["backupPath"]}')


def locate(name = None):
    #one way of method overloading
    #there is a overload module
    if(name == None):
        location = next((item for item in locations if item["game"] == game), False)
    else:
        location = next((item for item in locations if item["game"] == name), False)
    return location

def write():
    #note that if using r+ or a, it can leave dangling data
    #as it does not overwrite the file fully, and if json list is smaller
    #it will leave previous data
    with open(JSON_NAME, "w") as file:
        file.seek(0)
        json.dump(locations, file, indent=4, separators=(',',':'))
        file.close()
        
def check():
    location = locate()
    if(location == False):
        sys.exit(f'{game} paths have not been configured! Exiting...')
    global save_path
    save_path = location["savePath"]
    if(os.path.exists(save_path)==False):
        sys.exit("Save path not valid! Exiting...")
    global backup_path
    backup_path = location["backupPath"]
    if(os.path.exists(backup_path)==False):
        sys.exit("Backup path not valid! Exiting...")
    
def save():
    #create a folder in specified directory, named game name + date time saved
    check()
    #name time is folder name
    # game-year-month-day
    backup = f'{backup_path}/{nametime()}'
    move(save_path, backup)
    print(f'Saved {game} at {save_path} to {backup_path} in {nametime()}!')
     
def load(deleteBackup, deleteOld):
    #take files in saved0
    #way to select which backup to load
    #check backup directory for saves
    check()
    directory = os.listdir(backup_path)
    listSaves = []
    for x in directory:
        if(x.startswith(f'{game}-')==True):
            print(x)
            listSaves.append(x)
    print("List of backups in the configured backup folder")
    count = 0
    for x in listSaves:
        print(f'{count}: {x}')
        count += 1
    fileNum = int(input("Please select which backup you would like to load:"))
    if(fileNum >= len(listSaves)):
        sys.exit("Number given is out of range! Exiting...")
    folder = listSaves[fileNum]
    file = f'{backup_path}\{folder}'
    move(file, save_path)
    #check dates
    #print list of dates
    #user input which to load
    #load 
    print(f'{game} backup {folder} copied from {backup_path} to {save_path}')
    if(deleteBackup):
        overwrite = input(f'Are you sure you want to delete {folder} for {game} (y/n)?')
        if(overwrite.lower()=='n'):
            print("Aborted!")
        else:
            delete(file)
            print(f'Deleted backup {folder}')
    if(deleteOld):
        overwrite = input(f'Are you sure you want to delete all backups for {game} except for the latest (y/n)?')
        if(overwrite.lower()=='n'):
            print("Aborted!")
        else:
            latestFolder = listSaves.pop()
            for x in listSaves:
                delete(f'{backup_path}\{x}')
            print(f'Deleted all backups except for {latestFolder}')
        
def delete(file):
    shutil.rmtree(file)
    
def overwrite(text):
    print()
    
def move(source, dest):
    if(os.path.exists(dest)):
        #check if it is copying file from save to backup folder
        if(source == save_path):
            overwrite = input(f'{game} already has a backup on this date? Overwrite (y/n)?')
            #check lowercase in case a capital Y or N is input
            if(overwrite.lower()=='y'):
                shutil.rmtree(dest)
                shutil.copytree(source, dest)
            else:
                sys.exit("Backup aborted!")
        else:
            overwrite = input(f'Are you sure you want to load a backup from {source} to {dest} (y/n)?')
            if(overwrite.lower() == 'y'):
                #copytree default dirs_exist_ok == False
                shutil.copytree(source, dest, dirs_exist_ok=True)
            else:
                sys.exit("Aborting!")
    else:
        shutil.copytree(source, dest)
        
def nametime():
    #game name - year - month - day
    return f'{game}-{datetime.now().strftime("%Y-%m-%d")}'
            
def list():
    #list games with defined paths
    print("Listing existing game paths")
    for item in locations:
        print(item)

def parse_args():
    parser = argparse.ArgumentParser(description = 'Script to backup save games to another location')
    
    parser.add_argument('name',nargs = '?', help = "name of game to be saved")
    parser.add_argument('-l', '--list', action="store_true", help = "list all saved game paths")
    
    subparsers = parser.add_subparsers(title ='subcommands', help = 'add, change, save, load', dest='subcommand')
    
    a_parser = subparsers.add_parser("add", help = 'add new game paths')
    a_parser.add_argument('savepath', help = 'save path for files')
    a_parser.add_argument('backup', help = 'backup path')
    
    c_parser = subparsers.add_parser("change", help = 'change existing game paths')
    c_parser.add_argument('-cn', '--changename')
    c_parser.add_argument('-sp','--savepath')
    c_parser.add_argument('-bp','--backup')
    
    s_parser = subparsers.add_parser("save", help = 'backup save game')
    s_parser.add_argument('-t', '--title', help = 'name backup folder differently')
    
    l_parser = subparsers.add_parser("load", help = 'restore backup to save games')
    l_parser.add_argument('-db', '--deletebackup', action = "store_true", help = 'delete backup after loading')
    l_parser.add_argument('-do', '--deleteold', action = "store_true", help = 'delete all old backups and keep the newest backup')
    
    r_parser = subparsers.add_parser("remove", help = 'remove game path')
    r_parser.add_argument('-f', '--files', action= "store_true",help = 'delete all backups')
    
    return parser.parse_args()

if __name__ == "__main__":
    main()