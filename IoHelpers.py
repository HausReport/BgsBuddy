import inspect
import os
import json
import requests

from helpers.DailyPlan import DailyPlan
from helpers.DailyPlans import DailyPlans


def getDataFilePath(fName: str) -> str:
    cwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    cwd = os.path.join(cwd,fName)
    cwd = os.path.abspath(cwd)
    return cwd

def saveDailyPlans(fName: str, plans:DailyPlans):
    cwd = getDataFilePath(fName)
    text_file = open(cwd, "wt")
    n = text_file.write(plans.reprJSON())
    text_file.close()

def loadDailyPlans(fName:str) -> DailyPlans:
    cwd = getDataFilePath(fName)
    # reading the data from the file
    with open(cwd) as f:
        data = f.read()

    print("Data type before reconstruction : ", type(data))

    # reconstructing the data as a list of dictionaries
    js = json.loads(data)

    #print("Data type after reconstruction : ", type(js))
    #print(js)
    dp = DailyPlans()
    for item in js:
        if item=='foo':
            dp.setEtag(js['foo'])
            #print(f">{item}<")
        elif item=="plans":
            plz = js['plans']
            for pl in plz:
                adp = DailyPlan.fromDict(pl)
                dp.addPlan(adp)
    return dp

def downloadDailyPlans(fName="DailyPlans.json"):
    url = "https://raw.githubusercontent.com/HausReport/BgsBuddy/master/"+fName
    f = requests.get(url)

    etag: str = f.headers['Etag']

    print("DOWNLOADED JSON")
    print("===========================================")
    data = f.text
    print(data)
    # reconstructing the data as a list of dictionarues
    js = json.loads(data)

    dp = DailyPlans()
    dp.setEtag(etag)
    for item in js:
        adp = DailyPlan.fromDict(item)
        dp.addPlan(adp)
    return dp

