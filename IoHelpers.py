import inspect
import os
import json

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

    # reconstructing the data as a list of dictionarues
    js = json.loads(data)

    #print("Data type after reconstruction : ", type(js))
    #print(js)
    dp = DailyPlans()
    for item in js:
        adp = DailyPlan.fromDict(item)
        dp.addPlan(adp)
    return dp