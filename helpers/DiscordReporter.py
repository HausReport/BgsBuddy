import logging
import os
from typing import Dict

from .DailyPlan import DailyPlan
from .Status import Status
from .Reporter import Reporter
import requests
import json

class DiscordReporter(Reporter):
    def __init__(self, logger, hookUrl="https://discordapp.com/api/webhooks/784901136946561064/MyLLLTWbJnZWBAgGJlhDxe2rdYOE41qoc03hcNue_rzfWY8HGXayqyLE6VAeO0-72fW1"):
        self.logger = logger
        self.hook = hookUrl

    def report(self, ret: Status, plan: DailyPlan, event: Dict):
        if ret.getEffect() != 0:
            url = self.hook
            data = {}
            #for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
            data["content"] = ret.msg # "message content"
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