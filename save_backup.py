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
    
    global save_path
    global backup_path
    global locations
    locations = []
    
    #open json file containing game save paths
    with open(JSON_NAME, "r") as file:
        if(os.stat(JSON_PATH).st_size == 0): 
            #no json
            print("No existing game paths set up!")
            file.close()
        else:
        # print all existing games and paths
            locations = json.load(file)
            list()
            file.close()
    args = parse_args()
    game = args.name
    print(game)
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
    
    

def add(game):
    #use Tuple to save game name, save path, backup path?
    #need to check for duplicate game names!
    
    #check paths are valid
    if os.path.exists(save_path)==False:
        #sys.exit("save path not valid")
        print("save not valid")
    elif(os.path.exists(backup_path)==False):
        #sys.exit("backup path not valid")
        print("backup not valid")
    else:
        print("All paths valid!")
    new_json = {
        "game": game,
        "savePath": save_path,
        "backupPath": backup_path
    }
    with open(JSON_NAME, "r+") as file:
        locations.append(new_json)
        #file.seek(0)
        json.dump(locations, file, indent=4, separators=(',',':'))
        file.close()
    #save(game)
    #print("All  games in json file below:")
    #list()

def change():
    # figure out how to lookup and change
    # game
    # optional path
    # optional backup change
    #check that at least one is being changed
    print("change not implemented yet")
    
def save(game):
    
    print("Saved " + game + " to " + backup_path)
     
def load(game):
    #
    print("load not implemented")
    
def list():
    #list games with defined paths
    print("Existing game paths found!")

def parse_args():
    parser = argparse.ArgumentParser(description = 'Script to backup save games to another location')
    
    parser.add_argument('name', help = "name of game to be saved")
    
    subparsers = parser.add_subparsers(title ='subcommands', help = 'add, change, save, load', dest='subcommand')
    
    a_parser = subparsers.add_parser("add", help = 'add new game paths')
    a_parser.add_argument('savepath', help = 'save path for files')
    a_parser.add_argument('backup', help = 'backup path')
    
    c_parser = subparsers.add_parser("change", help = 'change existing game paths')
    c_parser.add_argument('name')
    #c_parser.add_argument('')
    #c_parser.add_argument('')
    #c_parser.add_argument('')
    
    s_parser = subparsers.add_parser("save", help = 'backup save game')
    s_parser.add_argument('name', help = 'game name')
    
    l_parser = subparsers.add_parser("load", help = 'restore backup to save games')
    l_parser.add_argument('name', help = 'game name')
    
    # parser.add_argument('-c', '--change', help = 'change existing game save paths')
    
    # parser.add_argument('-s', '--save', help = 'backup existing game saves')
    
    # parser.add_argument('-l', '--load', help = 'load existing backup to game')
    
    return parser.parse_args()

if __name__ == "__main__":
    main()