#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
#
# Portions adapted from BGS Tally v2.0 by Tez, made available under the MIT license below.
#
# MIT License
#
# Copyright (c) 2020 tezw21
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import logging
import os
import sys
import tkinter as tk
import webbrowser
from collections import OrderedDict
from pprint import pprint
from typing import Optional

import requests

import IoHelpers
from helpers.Target import Target

try:
    import myNotebook as nb
    from config import appname, config
except ImportError:
    pass

import GlobalDictionaries
from helpers.DiscordReporter import DiscordReporter

GlobalDictionaries.init_logger()
# GlobalDictionaries.load_addresses()

from helpers.DailyPlan import DailyPlan
from helpers.DailyPlans import DailyPlans
from helpers.LogReporter import LogReporter

logger = GlobalDictionaries.logger
logReporter: LogReporter = LogReporter(logger)
#logger.info("Test log msg")
#logging.info("This is a second log msg")

this = sys.modules[__name__]  # For holding module globals
this.VersionNo = "0.5"

class BgsBuddy:
    """
    ClickCounter implements the EDMC plugin interface.
    It adds a button to the EDMC UI that displays the number of times it has been clicked, and a preference to set
    the number directly.
    """

    def __init__(self) -> None:
        # Be sure to use names that wont collide in our config variables
        self.click_count: Optional[tk.StringVar] = tk.StringVar(value=str(config.getint('click_counter_count')))
        logger.info("BGS Buddy instantiated")

    def on_load(self) -> str:
        """
        on_load is called by plugin_start3 below.
        It is the first point EDMC interacts with our code after loading our module.
        :return: The name of the plugin, which will be used by EDMC for logging and for the settings window
        """
        return GlobalDictionaries.plugin_name

    def on_unload(self) -> None:
        """
        on_unload is called by plugin_stop below.
        It is the last thing called before EDMC shuts down. :1
        Note that blocking code here will hold the shutdown process.
        """
        self.on_preferences_closed("", False)  # Save our prefs

    def setup_preferences(self, parent: nb.Notebook, cmdr: str, is_beta: bool) -> Optional[tk.Frame]:
        """
        setup_preferences is called by plugin_prefs below.
        It is where we can setup our own settings page in EDMC's settings window. Our tab is defined for us.
        :param parent: the tkinter parent that our returned Frame will want to inherit from
        :param cmdr: The current ED Commander
        :param is_beta: Whether or not EDMC is currently marked as in beta mode
        :return: The frame to add to the settings window
        """
        current_row = 0
        frame = nb.Frame(parent)

        # setup our config in a "Click Count: number"
        nb.Label(frame, text='Click Count').grid(row=current_row)
        nb.Entry(frame, textvariable=self.click_count).grid(row=current_row, column=1)
        current_row += 1  # Always increment our row counter, makes for far easier tkinter design.
        return frame

    def on_preferences_closed(self, cmdr: str, is_beta: bool) -> None:
        """
        on_preferences_closed is called by prefs_changed below.
        It is called when the preferences dialog is dismissed by the user.
        :param cmdr: The current ED Commander
        :param is_beta: Whether or not EDMC is currently marked as in beta mode
        """
        #config.set('click_counter_count', self.click_count.get())
        pass

    def setup_main_ui(self, parent: tk.Frame) -> tk.Frame:
        # """
        # Create our entry on the main EDMC UI.
        # This is called by plugin_app below.
        # :param parent: EDMC main window Tk
        # :return: Our frame
        # """
        # current_row = 0
        # frame = tk.Frame(parent)
        # button = tk.Button(
        #     frame,
        #     text="Count me",
        #     command=lambda: self.click_count.set(str(int(self.click_count.get()) + 1))
        # )
        # button.grid(row=current_row)
        # current_row += 1
        # nb.Label(frame, text="Count:").grid(row=current_row, sticky=tk.W)
        # nb.Label(frame, textvariable=self.click_count).grid(row=current_row, column=1)
        # return frame
        pass

cc = BgsBuddy()

cmdrNameSet = False
dp = IoHelpers.downloadDailyPlans("DailyPlans.json")

dailyPlans: DailyPlans = dp
dailyPlans.addReporter(logReporter)
disco = DiscordReporter(logger)
dailyPlans.addReporter(disco)

print(dailyPlans.reprJSON())

#
# Direct EDMC callbacks to class
#

# Note that all of these could be simply replaced with something like:
# plugin_start3 = cc.on_load
def plugin_start3(plugin_dir: str) -> str:
    return cc.on_load()


def plugin_stop() -> None:
    return cc.on_unload()


def plugin_prefs(parent: nb.Notebook, cmdr: str, is_beta: bool) -> Optional[tk.Frame]:
    return cc.setup_preferences(parent, cmdr, is_beta)


def prefs_changed(cmdr: str, is_beta: bool) -> None:
    return cc.on_preferences_closed(cmdr, is_beta)


response = requests.get('https://api.github.com/repos/HausReport/BgsBuddy/releases/latest')  # check latest version
latest = response.json()
this.GitVersion = latest['tag_name']

logger.info(f"Current version: >{this.VersionNo}<, Latest version: >{this.GitVersion}<")
def plugin_app(parent: tk.Frame) -> Optional[tk.Frame]:
    # return cc.setup_main_ui(parent)
    """
    Create a frame for the EDMC main window
    """
    this.frame = tk.Frame(parent)

    Title = tk.Label(this.frame, text="BgsBuddy v" + this.VersionNo)
    Title.grid(row=0, column=0, sticky=tk.W)
    logger.info(f"Git Version: {this.GitVersion}, Current Version: {this.VersionNo}")
    if version_tuple(this.GitVersion) > version_tuple(this.VersionNo):
        title2 = tk.Label(this.frame, text="New version available", fg="blue", cursor="hand2")
        title2.grid(row=0, column=1, sticky=tk.W, )
        title2.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/HausReport/BgsBuddy/releases"))

    # tk.Button(this.frame, text='Data Today', command=display_data).grid(row=1, column=0, padx=3)
    # tk.Button(this.frame, text='Data Yesterday', command=display_yesterdaydata).grid(row=1, column=1, padx=3)
    # tk.Label(this.frame, text="Status:").grid(row=2, column=0, sticky=tk.W)
    # tk.Label(this.frame, text="Last Tick:").grid(row=3, column=0, sticky=tk.W)
    # this.StatusLabel = tk.Label(this.frame, text=this.Status.get())
    # this.StatusLabel.grid(row=2, column=1, sticky=tk.W)
    # this.TimeLabel = tk.Label(this.frame, text=tick_format(this.TickTime)).grid(row=3, column=1, sticky=tk.W)

    return this.frame

def version_tuple(version):
    try:
        ret = tuple(map(int, version.split(".")))
    except:
        ret = (0,)
    return ret

def journal_entry(cmdr, is_beta, system, station, entry, state):
    event = entry['event']

    if not cmdrNameSet:
        dailyPlans.setCommanderName(cmdr)

    if event == 'Docked' or (event == 'Location' and entry['Docked'] == True):
        stationFaction = entry['StationFaction']
        systemAddress = str(entry['SystemAddress'])
        systemName = entry['StarSystem']
        stationFactionName = stationFaction['Name']
        dailyPlans.setCurrentSystem(systemName)
        dailyPlans.setCurrentStation(station)
        dailyPlans.setCurrentStationFaction(stationFactionName)
        GlobalDictionaries.add_system_and_address(systemName, systemAddress)
        logger.info(f"Docked: Setting system={systemName}, station={station}, stationFaction={stationFaction}.")
        GlobalDictionaries.clear_target_dictionary()
    elif event == 'Undocked':
        dailyPlans.setCurrentStation(None)
        dailyPlans.setCurrentStationFaction(None)
        logger.info("Undocked: Setting station & stationFaction to none.")
    elif event == 'Location':
        systemName = entry['StarSystem']
        systemAddress = str(entry['SystemAddress'])
        dailyPlans.setCurrentSystem(systemName)
        dailyPlans.setCurrentStation(None)
        dailyPlans.setCurrentStationFaction(None)
        GlobalDictionaries.add_system_and_address(systemName, systemAddress)
        logger.info(f"Other location: Setting system={systemName}, station=None, stationFaction=None.")
    elif event == 'MissionCompleted':  # get mission influence value
        dailyPlans.checkMissionSuccess(entry)
        logger.info(f"Mission completed.")
    elif (event == 'SellExplorationData') or (event == 'MultiSellExplorationData'):  # get carto data value
        dailyPlans.checkCartography(entry)
        logger.info(f"Sell Exploration Data.")
    elif event == 'RedeemVoucher' and entry['Type'] == 'bounty':  # bounties collected
        dailyPlans.checkBounty(entry)
        logger.info(f"Redeem Bounty.")
    elif event == 'RedeemVoucher' and entry['Type'] == 'CombatBond':  # bonds collected
        dailyPlans.checkBond(entry)
        logger.info(f"Redeem Bond.")
    elif event == 'MarketSell':  # Trade Profit
        dailyPlans.checkTrade(entry)
        logger.info(f"Trade.")
    elif event == 'ShipTargeted':  # Target ship
        # { "timestamp":"2020-11-12T22:09:36Z", "event":"ShipTargeted", "TargetLocked":true,
        # "Ship":"python", "ScanStage":3, "PilotName":"$ShipName_Police_Federation;",
        # "PilotName_Localised":"Federal Security Service", "PilotRank":"Competent",
        # "ShieldHealth":100.000000, "HullHealth":100.000000,
        # "Faction":"Pleiades Resource Enterprise", "LegalStatus":"Clean" }

        if 'PilotName_Localised' in entry and 'Faction' in entry:
            pilotName = entry['PilotName_Localised']
            pilotFaction = entry['Faction']
            logger.info(f"Targeted: {pilotName} from {pilotFaction}")
            ship = "Unknown"
            if 'Ship' in entry:
                ship = entry['Ship']
            rank = "Unknown"
            if 'PilotRank' in entry:
                rank = entry['PilotRank']
            targ: Target = Target(pilotName, pilotFaction, ship, rank)
            GlobalDictionaries.add_target_faction(pilotName, targ)
    elif event == 'CommitCrime' and entry['CrimeType'] == 'murder':  # Clean Murder
        dailyPlans.checkMurder(entry)
    elif event == 'SendText':
        # {"timestamp": "2020-12-08T23:32:07Z", "event": "SendText", "To": "Dan Sho", "Message": "sweet :)",
        #   "Sent"     : true}
        msg: str = entry['Message']
        KEY = 'anticlub'
        KEYR = 'антиклуб'
        logger.info(f'Message: >{msg}<')
        if msg.startswith(KEY):
            dailyPlans.sendMessage(entry, msg[len(KEY):])
        elif  msg.startswith(KEYR):
            dailyPlans.sendMessage(entry, msg[len(KEYR):])
    elif event == 'FSDJump' or event == 'CarrierJump':  # get factions at jump
        #
        # Update system stuff
        #
        systemName = entry['StarSystem']
        systemAddress = str(entry['SystemAddress'])
        dailyPlans.setCurrentSystem(systemName)
        dailyPlans.setCurrentStation(None)
        dailyPlans.setCurrentStationFaction(None)
        GlobalDictionaries.add_system_and_address(systemName, systemAddress)
        logger.info(f"{event}: Setting system={systemName}, station=None, stationFaction=None.")

        GlobalDictionaries.clear_target_dictionary()

        pprint(entry['Factions'])
        # for fac in entry['factions']:
        #     faction: OrderedDict = fac
        #     print(faction['Name'])
        #     print(faction['FactionState'])
        #     print(faction['Government'])
        #     print(faction['Influence'])
        #     print(faction['Allegiance'])
        #     print(faction['MyReputation'])
        #     for activeState in faction['ActiveStates']:
        #         print(activeState[1])

    # FIXME: Not sure we'd need list of local faction names
    # FIXME: Having a list of faction states, however would be useful for
    # boom/investment bonuses, detecting war/civil war/exotic states
    #
    # Update faction stuff
    #
    # this.FactionNames = []
    # this.FactionStates = {'Factions': []}
    # z = 0
    # for i in entry['Factions']:
    #     if i['Name'] == "Pilots' Federation Local Branch":
    #         continue
    #
    #     this.FactionNames.append(i['Name'])
    #     this.FactionStates['Factions'].append(
    #         {'Faction': i['Name'], 'Happiness': i['Happiness_Localised'], 'States': []})
    #
    #     try:
    #         for x in i['ActiveStates']:
    #             this.FactionStates['Factions'][z]['States'].append({'State': x['State']})
    #     except KeyError:
    #         this.FactionStates['Factions'][z]['States'].append({'State': 'None'})
    #     z += 1



# Structure of entry['factions']:
#
# [OrderedDict([('Name', 'Sirius Corporation'),
#               ('FactionState', 'Investment'),
#               ('Government', 'Corporate'),
#               ('Influence', 0.422422),
#               ('Allegiance', 'Independent'),
#               ('Happiness', '$Faction_HappinessBand1;'),
#               ('Happiness_Localised', 'Elated'),
#               ('MyReputation', -99.233101),
#               ('ActiveStates',
#                [OrderedDict([('State', 'Investment')]),
#                 OrderedDict([('State', 'CivilLiberty')])])]),
#  OrderedDict([('Name', 'Luyten 674-15 Industries'),
#               ('FactionState', 'PirateAttack'),
#               ('Government', 'Corporate'),
#               ('Influence', 0.039039),
#               ('Allegiance', 'Independent'),
#               ('Happiness', '$Faction_HappinessBand2;'),
#               ('Happiness_Localised', 'Happy'),
#               ('MyReputation', 0.0),
#               ('ActiveStates', [OrderedDict([('State', 'PirateAttack')])])]),



#
# Missions event
#
# {
#   "timestamp": "2020-12-12T17:12:29Z",
#   "event": "Missions",
#   "Active": [
#     {
#       "MissionID": 674018559,
#       "Name": "MISSION_Salvage_Refinery_name",
#       "PassengerMission": false,
#       "Expires": 363122
#     },
#     {
#       "MissionID": 674357771,
#       "Name": "MISSION_Disable_BLOPS_name",
#       "PassengerMission": false,
#       "Expires": 253814
#     },


#
# After killing a CZ ship
# Note: this gives an absolute answer to who the war is against
#
# {
#   "timestamp": "2020-12-12T17:15:08Z",
#   "event": "FactionKillBond",
#   "Reward": 31113,
#   "AwardingFaction": "New Solati Liberals",
#   "VictimFaction": "Hodack Prison Colony"
# }
#
# When targeting a CZ ship
#
# {
#   "timestamp": "2020-12-12T17:15:54Z",
#   "event": "ShipTargeted",
#   "TargetLocked": true,
#   "Ship": "vulture",
#   "ScanStage": 3,
#   "PilotName": "$ShipName_Military_Independent;",
#   "PilotName_Localised": "System Defence Force",
#   "PilotRank": "Dangerous",
#   "ShieldHealth": 0,
#   "HullHealth": 95.307114,
#   "Faction": "Hodack Prison Colony",
#   "LegalStatus": "Lawless"
# }

#
# When the game is shut down
#
# {
#   "timestamp": "2020-12-12T17:20:04Z",
#   "event": "Shutdown"
# }

#
# When the game is started up
#
# {
#   "timestamp": "2020-12-12T17:12:22Z",
#   "event": "LoadGame",
#   "FID": "ZZZZZZ",
#   "Commander": "Erlaed",
#   "Horizons": true,
#   "Ship": "Federation_Corvette",
#   "Ship_Localised": "Federal Corvette",
#   "ShipID": 32,
#   "ShipName": "bounty",
#   "ShipIdent": "HR-42A",
#   "FuelLevel": 32,
#   "FuelCapacity": 32,
#   "GameMode": "Solo",
#   "Credits": 4576786079,
#   "Loan": 0
# }

#
# Accepting a mission
#
# {
#   "timestamp": "2020-12-12T19:45:41Z",
#   "event": "MissionAccepted",
#   "Faction": "New Solati Liberals",
#   "Name": "Mission_Massacre_Conflict_CivilWar",
#   "LocalisedName": "Massacre Hodack Prison Colony ships",
#   "TargetFaction": "Hodack Prison Colony",
#   "KillCount": 64,
#   "DestinationSystem": "Solati",
#   "DestinationStation": "Solati Reach",
#   "Expiry": "2020-12-13T16:32:55Z",
#   "Wing": false,
#   "Influence": "++",
#   "Reputation": "++",
#   "Reward": 31797020,
#   "MissionID": 675213488
# }

