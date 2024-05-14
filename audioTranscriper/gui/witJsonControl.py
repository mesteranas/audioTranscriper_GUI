import json,os
import settings
path=os.path.join(os.getenv('appdata'),settings.app.appName,"wit.json")
if not os.path.exists(path):
    with open(path,"w") as file:
        file.write("{}")
def get():
    with open(path,"r",encoding="utf-8")as data:
        return json.load(data)
def save(data):
    with open(path,"w",encoding="utf-8") as file:
        file.write(str(data).replace("'",'"'))