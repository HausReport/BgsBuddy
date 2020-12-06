import logging
import os
from typing import Dict

from .DailyPlan import DailyPlan
from .Status import Status
from .Reporter import Reporter
import requests
import json

#Adapted from https://gist.github.com/Bilka2/5dd2ca2b6e9f3573e0c2defe5d3031b2

class DiscordReporter(Reporter):
    def __init__(self, logger):
        self.logger = logger
        #self.hook = hookUrl

    def report(self, ret: Status, plan: DailyPlan, event: Dict):
        if ret.getEffect() != 0:
            url = ret.getHookUrl() # self.hook
            data = {}
            #for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
            data["content"] = self.getCommanderName() + " : " + ret.msg # "message content"
            data["username"] = "EDMC Plugin" #"custom username"

            #leave this out if you dont want an embed
            #data["embeds"] = []
            #embed = {}
            #for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
            #embed["description"] = "text in embed"
            #embed["title"] = "embed title"
            #data["embeds"].append(embed)

            result = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})

            try:
                result.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print(err)
            else:
                print("Payload delivered successfully, code {}.".format(result.status_code))

#result: https://i.imgur.com/DRqXQzA.png