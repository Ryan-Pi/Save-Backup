import os
import shutil
import argparse
import datetime
import json

# python script with config file

def main():
    
    global save_path
    global backup_path
    global file
    global locations
    
    #open json file containing game save paths
    with open("games.json", "r") as file:
        if(file.read() == ''):
            #no json
            print("No existing game paths set up!")
        else:
        # print all existing games and paths
            print("Existing game paths found!")
            list()
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
    new_json = {
        "game": game,
        "savePath": save_path,
        "backupPath": backup_path
    }
    with open("games.json", "a+") as file:
        locations = json.load(file)
        json.dump(new_locations, file)
        new_locations = locations.append(new_json)
    #json.dump(new_json, file)
    #if os.path.exists(dest)
    print("yes")

def change():
    print("")
    
def save(game):
    print("")   
     
def load(game):
    #
    print("")
    
def list():
    #list games with defined paths
    print("Existing game paths found!")

def parse_args():
    parser = argparse.ArgumentParser(description = 'Script to backup save games to another location')
    
    parser.add_argument('name', help = "name of game to be saved")
    
    subparsers = parser.add_subparsers(title ='subcommands', help = 'add, change, save, load', dest='subcommand')
    
    a_parser = subparsers.add_parser("add", help = 'add')
    a_parser.add_argument('savepath', help = 'save path for files')
    a_parser.add_argument('backup', help = 'backup path')
    
    # parser.add_argument('-a', '--add', help = 'add new game and paths')
    
    # parser.add_subparsers('-n')
    
    # parser.add_subparsers('-sp')
    
    # parser.add_subparsers('-bp')
    
    # parser.add_argument('-c', '--change', help = 'change existing game save paths')
    
    # parser.add_argument('-s', '--save', help = 'backup existing game saves')
    
    # parser.add_argument('-l', '--load', help = 'load existing backup to game')
    
    return parser.parse_args()

if __name__ == "__main__":
    main()