import json
import os   

FILE_NAME = "games.json"

new_json = {
    "game": "gamesaras",
    "savePath": "save_path",
    "backupPath": "backup_path"
    }
new_jsons = []
with open("games.json", "r+") as file:
    filepath = os.getcwd() + "\\" + FILE_NAME
    if(os.stat(filepath).st_size != 0): 
        new_jsons = json.load(file)
    new_jsons.append(new_json)
    file.seek(0)
    json.dump(new_jsons, file, indent=4, separators=(',',':'))
    file.close()