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
        print(save_path)
        print(backup_path)
        add(game)
    elif args.subcommand == 'change':
        change(game)
    elif args.subcommand == 'save':
        save(game)
    elif args.subcommand == 'load':
        load(game)
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
    list()

def change():
    # figure out how to lookup and change
    # game
    # optional path
    # optional backup change
    #check that at least one is being changed
    print("change not implemented yet")
    
def remove():
    #remove an entry
    location = next((item for item in locations if item["game"] == game), True)
    if(location):
        sys.exit(game + " path does not exist!")
    for x in locations:
         if(x == location):
            locations.remove(x)
    write()
    print("Removed entry for " + game + " with save path " + save_path + " and backup path " + backup_path)

def write():
    #fill this with open as file, 
    with open(JSON_NAME, "r+") as file:
        file.seek(0)
        json.dump(locations, file, indent=4, separators=(',',':'))
        file.close()
    
def save():
    
    print("Saved " + game + " to " + backup_path)
     
def load():
    #
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
    #c_parser.add_argument('name')
    c_parser.add_argument('--savepath')
    c_parser.add_argument('--backup')
    
    s_parser = subparsers.add_parser("save", help = 'backup save game')
    
    l_parser = subparsers.add_parser("load", help = 'restore backup to save games')
    
    r_parser = subparsers.add_parser("remove", help = 'remove game path')
    
    return parser.parse_args()

if __name__ == "__main__":
    main()