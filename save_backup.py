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
import datetime
import json

# python script with json file that saves game paths

JSON_NAME = "games.json"
JSON_PATH = os.getcwd() + "\\" + JSON_NAME

def main():
    
    global game
    global save_path
    global backup_path
    global locations
    global empty
    locations = []
    
    #open json file containing game save paths
    with open(JSON_NAME, "r") as file:
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
    if(args.list):
        list()
        #sys.exit()
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
        load()
    elif args.subcommand == 'remove':
        remove(args.files)
    # path to find saves
    # path to backup saves
    # command to list games, with path settings saved?
    # command to add games with path settings
    # create folder in specified backup directory, with saves, named date + time
    
    

def add():
    #use Tuple to save game name, save path, backup path?
    #need to check for duplicate game names!
    if(next((item for item in locations if item["game"] == game), False)):
        sys.exit(game + " path already exists!")
    #check paths are valid
    if (os.path.exists(save_path)==False):
        sys.exit("save path not valid")
    elif(os.path.exists(backup_path)==False):
        sys.exit("backup path not valid")
    else:
        print("All paths valid!")
    new_json = {
        "game": game,
        "savePath": save_path,
        "backupPath": backup_path
    }
    locations.append(new_json)
    write()
    print(game + " added successfully!")
    list()

def change(name, save, back):
    #add flag to move previous backups to new directory
    # remove old one, add new one
    # python makes shallow copies, so modifying location
    # will change the dict in locations list
    location = locate()
    if(location == False):
        #exit if no such game has been saved 
        sys.exit(game + " has not been added!")
    # optional path
    if(name != None):
        newName = locate(name)
        if(newName == False):
            #checks if an entry for the proposed name change already exists
            location["game"] = name
        else:
            sys.exit(name + " has already been configured with save path " + newName["savePath"] + " and backup path " + newName["backupPath"])
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
    print("Change successful!")
    list()
    
def remove(delFiles):
    #remove an entry
    location = locate()
    if(location == False):
        sys.exit(game + " entry does not exist!")
    for x in locations:
         if(x == location):
            locations.remove(x)
    #write()
    print("Removed entry for " + game + " with save path " + location["savePath"] + " and backup path " + location["backupPath"])
    #add option to delete all back ups for a game
    if(delFiles==True):
        #delete all backup files for game name
        print("Removed all files for " + game + " from " + location["backupPath"])


def locate(name = None):
    #one way of method overloading
    #there is a overload module
    if(name == None):
        location = next((item for item in locations if item["game"] == game), False)
    else:
        location = next((item for item in locations if item["game"] == name), False)
    return location

def write():
    #fill this with open as file, 
    with open(JSON_NAME, "r+") as file:
        file.seek(0)
        json.dump(locations, file, indent=4, separators=(',',':'))
        file.close()
    
def save():
    #create a folder in specified directory, named game name + date time saved
    print("Saved " + game + " to " + backup_path)
     
def load():
    #take files in saved
    #way to select which backup to load
    print("load not implemented")
    
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
    
    r_parser = subparsers.add_parser("remove", help = 'remove game path')
    r_parser.add_argument('-f', '--files', action= "store_true",help = 'delete all backups')
    
    return parser.parse_args()

if __name__ == "__main__":
    main()