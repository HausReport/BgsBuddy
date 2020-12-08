#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
#
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
# System Name
# Hero Faction
# Target Faction
# Discord Webhook?


# === Positive Levers ===
# Mission Completion (ez)              -- ALWAYS
# Bounties (ez)                        -- OPTIONAL
# Cartographic Data (ez)               -- OPTIONAL
# Trade at Profit (ez)                 -- OPTIONAL

# === Negative Levers ===
# Mission Fails (needs backing table)  -- ALWAYS
# Trade at Loss (ez)                   -- OPTIONAL
# Clean Murders (needs backing table)  -- ALWAYS

# === Special Circumstances
# War - Bonds
# War - CZ Wins
# War - Bounties
# Election?
# Draught?
# Infrastructure Failure?
# Other states?
import logging
from typing import List, Dict

from .Status import Status

# from ..GlobalDictionaries import *
try:
    import GlobalDictionaries
except ImportError:
    from .. import GlobalDictionaries

import json

CAT_MISSION_SUCCESS = "MissionSuccess"
CAT_BOUNTY = "Bounty"
CAT_CARTOGRAPHY = "Cartography"
CAT_TRADE_PROFIT = "TradeProfit"
CAT_TRADE_LOSS = "TradeLoss"
CAT_MISSION_FAIL = "MissionFail"
CAT_MURDER = "Murder"

DEFAULT_HOOK_URL = "https://discordapp.com/api/webhooks/784901136946561064/MyLLLTWbJnZWBAgGJlhDxe2rdYOE41qoc03hcNue_rzfWY8HGXayqyLE6VAeO0-72fW1"


class DailyPlan:
    #
    # Plan statics
    #
    systemName = None
    heroFaction = None
    targetFaction = None

    #
    # Movement based
    #
    currentSystem = None
    currentSystemFactions = None
    currentStation = None
    currentStationFaction = None

    #
    # Goals
    #
    missionInfluenceGoal = 0
    bountyGoal = 0
    cartographyGoal = 0
    tradeProfitGoal = 0
    missionFailGoal = 0
    tradeLossGoal = 0
    murderGoal = 0

    def __init__(self, systemName, heroFaction, targetFaction):
        self.systemName = systemName
        self.heroFaction = heroFaction
        self.targetFaction = targetFaction
        # import GlobalDictionaries  # NOTE: this is fucked, but only way it works with edmc unless i put code in a different git
        self.logger = GlobalDictionaries.logger
        self.logger.info("Initialized DailyPlan")
        self.logger.debug('This message should go to the log file')
        self.logger.info('So should this')
        self.logger.warning('And this, too')
        self.logger.error('And non-ASCII stuff, too, like Øresund and Malmö')
        self.hookUrls: List[str] = []  # DEFAULT_HOOK_URL

    def currentlyInTargetSystem(self) -> bool:
        return self.isSystemName(self.currentSystem)

    def isSystemName(self, name: str) -> bool:
        if self.systemName is None:
            return False
        if name is None:
            return False
        return name.lower() == self.systemName.lower()

    def isHeroFactionName(self, name: str) -> bool:
        if self.heroFaction is None:
            return False
        if name is None:
            return False
        return name.lower() == self.heroFaction.lower()

    def isTargetFactionName(self, name: str) -> bool:
        if self.targetFaction is None:
            return False
        if name is None:
            return False
        return name.lower() == self.targetFaction.lower()

    def isNeitherFactionName(self, name: str) -> bool:
        if not self.isHeroFactionName(name):
            if not self.isTargetFactionName(name):
                return True
        return False

    def addHookUrl(self, url: str):
        self.hookUrls.append(url)

    #
    # Updated by DailyPlans as ship moves
    #
    def setCurrentSystem(self, sys: str):
        self.currentSystem: str = sys

    def setCurrentSystemFactions(self, facs: List[str]):
        self.currentSystemFactions: List[str] = facs

    def setCurrentStation(self, sta: str):
        self.currentStation: str = sta

    def setCurrentStationFaction(self, fac: str):
        self.currentStationFaction: str = fac

    #
    # Positive Levers
    #
    def addMissionInfluenceGoal(self, miss: int = 60):
        self.missionInfluenceGoal = miss

    def addBountyGoal(self, bounty: int = 4000000):
        self.bountyGoal = bounty

    def addCartographyGoal(self, cart: int = 12000000):
        self.cartographyGoal = cart

    def addTradeProfitGoal(self, prof: int = 16000000):
        self.tradeProfitGoal = prof

    #
    # Negative Levers
    #
    def addMissionFailGoal(self, miss: int = 12):
        self.missionFailGoal = miss

    def addTradeLossGoal(self, loss: int = 16000000):
        self.tradeLossGoal = loss

    def addMurderGoal(self, murd: int = 12):
        self.murderGoal = murd

    #
    # Lever checks
    # return -1 for harmful action
    # return 0 for neutral action
    # return +1 for helpful action
    #
    def checkMissionSuccess(self, entry: Dict) -> List[Status]:
        ret: List[Status] = []
        factionEffects = entry['FactionEffects']
        print(json.dumps(factionEffects))

        for effect in factionEffects:
            factionName = effect['Faction']
            influenceEntries = effect['Influence']
            print(factionName)
            for influenceEntry in influenceEntries:
                entrySystemAddress = str(influenceEntry['SystemAddress'])
                # from .. import GlobalDictionaries HERE
                # import GlobalDictionaries
                entrySystemName = GlobalDictionaries.get_system_by_address(entrySystemAddress)
                self.logger.info(
                    f"SystemAddress: {entrySystemAddress}, SystemName: {entrySystemName}, curSys: {self.systemName}")
                infStr: str = influenceEntry['Influence']
                inf: int = len(infStr)
                infSign: int = 1
                if infStr.startswith("-"):
                    infSign = -1
                inf = inf * infSign
                if self.isSystemName(entrySystemName):  # FIXME: revisit case of two systems with same name
                    if inf > 0:
                        if self.isHeroFactionName(factionName):
                            msg = f"{self.systemName}: {factionName}: Mission Contribution: {inf} points."
                            self.logger.info(msg)
                            ret.append(Status(1, msg, CAT_MISSION_SUCCESS, inf, self.hookUrls))
                        elif self.isTargetFactionName(factionName):
                            msg = f"{self.systemName}: {factionName}: Mission Contribution to **ENEMY**: {inf} points."
                            self.logger.info(msg)
                            ret.append(Status(-1, msg, CAT_MISSION_SUCCESS, inf, self.hookUrls))
                        else:
                            msg = f"{self.systemName}: {factionName}: Mission Contribution to **COMPETITOR**: {inf} points."
                            self.logger.info(msg)
                            ret.append(Status(-1, msg, CAT_MISSION_SUCCESS, inf, self.hookUrls))
                    elif inf < 0:
                        if self.isHeroFactionName(factionName):
                            msg = f"{self.systemName}: {factionName}: Negative Mission Contribution to **ALLY**: {inf} points."
                            self.logger.info(msg)
                            ret.append(Status(-1, msg, CAT_MISSION_SUCCESS, inf, self.hookUrls))
                        elif self.isTargetFactionName(factionName):
                            msg = f"{self.systemName}: {factionName}: Negative Mission Contribution to ENEMY: {inf} points."
                            self.logger.info(msg)
                            ret.append(Status(1, msg, CAT_MISSION_SUCCESS, inf, self.hookUrls))
                        else:
                            msg = f"{self.systemName}: {factionName}: Negative Mission Contribution to **COMPETITOR**: {inf} points."
                            self.logger.info(msg)
                            ret.append(Status(-1, msg, CAT_MISSION_SUCCESS, inf, self.hookUrls))

        return ret

    def checkBounty(self, entry: Dict) -> List[Status]:
        ret: List[Status] = []
        if self.currentlyInTargetSystem():
            for z in entry['Factions']:
                factionName = z['Faction']
                bounty = z['Amount']
                if self.isHeroFactionName(factionName):
                    msg = f"{self.systemName}: {factionName}: Bounty contribution of {bounty:,} credits."
                    ret.append(Status(1, msg, CAT_BOUNTY, bounty, self.hookUrls))
                elif self.isTargetFactionName(factionName):
                    msg = f"{self.systemName}: {factionName}: Bounty contribution of to **ENEMY** of {bounty:,} credits."
                    ret.append(Status(-1, msg, CAT_BOUNTY, bounty, self.hookUrls))
                else:
                    msg = f"{self.systemName}: {factionName}: Bounty contribution of to **COMPETITOR** of {bounty:,} credits."
                    ret.append(Status(-1, msg, CAT_BOUNTY, bounty, self.hookUrls))
        return ret

    def checkCartography(self, entry: Dict) -> List[Status]:
        ret: List[Status] = []
        if self.currentlyInTargetSystem():
            factionName = self.currentStationFaction
            if factionName is not None:
                earnings: int = int(entry['TotalEarnings'])
                if self.isHeroFactionName(factionName):
                    msg = f"{self.systemName}: {factionName}: Exploration data sold: {earnings:,} ."
                    ret.append(Status(1, msg, CAT_CARTOGRAPHY, earnings, self.hookUrls))
                elif self.isTargetFactionName(factionName):
                    msg = f"{self.systemName}: {factionName}: Exploration data sold to **ENEMY**: {earnings:,} ."
                    ret.append(Status(-1, msg, CAT_CARTOGRAPHY, earnings, self.hookUrls))
                else:
                    msg = f"{self.systemName}: {factionName}: Exploration data sold to **COMPETITOR**: {earnings:,} ."
                    ret.append(Status(-1, msg, CAT_CARTOGRAPHY, earnings, self.hookUrls))
        return ret

    def checkTrade(self, entry: Dict) -> List[Status]:
        ret: List[Status] = []
        if self.currentlyInTargetSystem():
            factionName = self.currentStationFaction
            if factionName is not None and factionName != "FleetCarrier":
                count: int = int(entry['Count'])
                cost: int = count * int(entry['AvgPricePaid'])
                profit: int = int(entry['TotalSale']) - cost
                commodity: str = entry['Type']
                if profit > 0:
                    if self.isHeroFactionName(factionName):
                        msg = f"{self.systemName}: {factionName}: Trade For Profit: {profit:,} ({count} of {commodity})."
                        ret.append(Status(1, msg, CAT_TRADE_PROFIT, profit, self.hookUrls))
                    elif self.isTargetFactionName(factionName):
                        msg = f"{self.systemName}: {factionName}: Trade For Profit **ENEMY** : {profit:,} ({count} of {commodity})."
                        ret.append(Status(-1, msg, CAT_TRADE_PROFIT, profit, self.hookUrls))
                    else:
                        msg = f"{self.systemName}: {factionName}: Trade For Profit **COMPETITOR** : {profit:,} ({count} of {commodity})."
                        ret.append(Status(-1, msg, CAT_TRADE_PROFIT, profit, self.hookUrls))
                else:
                    if self.isTargetFactionName(factionName):
                        msg = f"{self.systemName}: {factionName}: Trade For Loss: {profit:,} ({count} of {commodity})."
                        ret.append(Status(1, msg, CAT_TRADE_LOSS, profit, self.hookUrls))
                    elif self.isHeroFactionName(factionName):
                        msg = f"{self.systemName}: {factionName}: Trade For Loss **ALLY**: {profit:,} ({count} of {commodity})."
                        ret.append(Status(-1, msg, CAT_TRADE_LOSS, profit, self.hookUrls))
                    else:
                        msg = f"{self.systemName}: {factionName}: Trade For Loss **COMPETITOR**: {profit:,} ({count} of {commodity})."
                        ret.append(Status(-1, msg, CAT_TRADE_LOSS, profit, self.hookUrls))

        return ret

    def checkMissionFail(self, event: Dict) -> List[Status]:
        ret: List[Status] = []
        a = 4
        #
        # If attacks enemy faction in goal system
        #
        if a == 0:
            ret.append(Status(1, "Failed Mission against Enemy Faction", CAT_MISSION_FAIL, 1, self.hookUrls))

        #
        # If benefits hero faction in goal system
        #
        if a == 0:
            ret.append(Status(-1, "Failed Mission against Hero Faction", CAT_MISSION_FAIL, 1, self.hookUrls))

        #
        # If benefits competitor faction in goal system
        #
        if a == 0:
            ret.append(Status(-1, "Failed Mission against Neutral Faction", CAT_MISSION_FAIL, 1, self.hookUrls))

        return ret

    def checkMurder(self, event: Dict) -> List[Status]:
        ret: List[Status] = []
        self.logger.info("In checkMurder")
        if self.currentlyInTargetSystem():
            self.logger.info("In checkMurder: system good")
            pilotName = event['Victim']
            import GlobalDictionaries
            pilotFaction = GlobalDictionaries.get_target_faction(pilotName)

            if pilotFaction is None:
                self.logger.error(f"Unknown pilot faction in murder check")
            elif self.isTargetFactionName(pilotFaction):
                ret.append(
                    Status(1, f"{self.systemName}: {pilotFaction}: Murdered Enemy", CAT_MURDER, 1, self.hookUrls))
            elif self.isHeroFactionName(pilotFaction):
                ret.append(
                    Status(-1, f"{self.systemName}: {pilotFaction}: Murdered **ALLY**", CAT_MURDER, 1, self.hookUrls))
            else:
                ret.append(Status(-1, f"{self.systemName}: {pilotFaction}: Murdered **BYSTANDER**", CAT_MURDER, 1,
                                  self.hookUrls))

        return ret

    #
    # Marshalling/unmarshalling of plans as JSON(L)
    #
    def reprJSON(self):
        d = dict()
        for a, v in self.__dict__.items():
            if a == "logger":
                continue
            elif (hasattr(v, "reprJSON")):
                d[a] = v.reprJSON()
            else:
                d[a] = v
        return json.dumps(d, indent=4)
    #    return d
    # default = lambda o: f"<<non-serializable: {type(o).__qualname__}>>"

    @staticmethod
    def fromDict(aDict: Dict[str, str]):
        systemName = None
        heroFaction=None
        targetFaction=None

        if "systemName" in aDict:
            systemName = aDict.get("systemName")
        if "heroFaction" in aDict:
            heroFaction = aDict.get("heroFaction")
        if "systemName" in aDict:
            targetFaction = aDict.get("targetFaction")

        if systemName is None or heroFaction is None or targetFaction is None:
            return None

        ret: DailyPlan = DailyPlan(systemName,heroFaction,targetFaction)

        if "missionInfluenceGoal" in aDict:
            ret.addMissionInfluenceGoal(aDict.get("missionInfluenceGoal"))
        if "bountyGoal" in aDict:
            ret.addBountyGoal(aDict.get("bountyGoal"))
        if "cartographyGoal" in aDict:
            ret.addCartographyGoal(aDict.get("cartographyGoal"))
        if "tradeProfitGoal" in aDict:
            ret.addTradeProfitGoal(aDict.get("tradeProfitGoal"))
        if "missionFailGoal" in aDict:
            ret.addMissionFailGoal(aDict.get("missionFailGoal"))
        if "tradeLossGoal" in aDict:
            ret.addTradeLossGoal(aDict.get("tradeLossGoal"))
        if "murderGoal" in aDict:
            ret.addMurderGoal(aDict.get("murderGoal"))
        if "hookUrls" in aDict:
            strs: List[str] = aDict.get("hookUrls")
            for it in strs:
                ret.addHookUrl(it)

        return ret

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

