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
from typing import List, Dict

from .Status import Status
#from ..GlobalDictionaries import *

CAT_MISSION_SUCCESS = "MissionSuccess"
CAT_BOUNTY = "Bounty"
CAT_CARTOGRAPHY = "Cartography"
CAT_TRADE_PROFIT = "TradeProfit"
CAT_TRADE_LOSS = "TradeLoss"
CAT_MISSION_FAIL = "MissionFail"
CAT_MURDER = "Murder"


class DailyPlan:
    #
    # Plan statics
    #
    systemName = None
    # systemAddress = None
    heroFaction = None
    targetFaction = None

    #
    # Movement based
    #
    currentSystem = None
    # currentSystemAddress = None
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

    def currentlyInTargetSystem(self) -> bool:
        return self.isSystemName(self.currentSystem)

    def isSystemName(self, name: str) -> bool:
        return name.lower() == self.systemName.lower()

    def isHeroFactionName(self, name: str) -> bool:
        return name.lower() == self.heroFaction.lower()

    def isTargetFactionName(self, name: str) -> bool:
        return name.lower() == self.targetFaction.lower()

    def isNeitherFactionName(self, name: str) -> bool:
        if not self.isHeroFactionName(name):
            if not self.isTargetFactionName(name):
                return True
        return False

    #
    # Updated by DailyPlans as ship moves
    #
    def setCurrentSystem(self, sys: str):
        self.currentSystem: str = sys
        # self.currentSystemAddress: str = add
        #
        # FIXME: Not sure if this makes sense
        # Say that you log in in a different system and submit a mission,
        # the systemAddress may not have been set.
        # Maybe initialize systemaddresses when getting the missions event?
        #
        # if self.isSystemName(sys):
        # if self.systemAddress is None:
        # self.systemAddress = add

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

        for effect in factionEffects:
            factionName = effect['Faction']
            influenceEntries = effect['Influence']
            print(factionName)
            for influenceEntry in influenceEntries:
                entrySystemAddress = str(influenceEntry['SystemAddress'])
                from .. import GlobalDictionaries
                entrySystemName = GlobalDictionaries.get_system_by_address(entrySystemAddress)
                inf = len(influenceEntry['Influence'])
                if self.isSystemName(entrySystemName):  # FIXME: revisit case of two systems with same name
                    if self.isHeroFactionName(factionName):
                        msg = f"Mission Contribution for Hero Faction {factionName} of {inf} points."
                        ret.append(Status(1, msg, CAT_MISSION_SUCCESS, inf))
                    elif self.isTargetFactionName(factionName):
                        msg = f"Mission Contribution for Target Faction {factionName} of {inf} points."
                        ret.append(Status(-1, msg, CAT_MISSION_SUCCESS, inf))
                    else:
                        msg = f"Mission Contribution for Competitor Faction {factionName} of {inf} points."
                        ret.append(Status(-1, msg, CAT_MISSION_SUCCESS, inf))

        return ret

    def checkBounty(self, entry: Dict) -> List[Status]:
        ret: List[Status] = []
        if self.currentlyInTargetSystem():
            for z in entry['Factions']:
                factionName = z['Faction']
                bounty = z['Amount']
                if self.isHeroFactionName(factionName):
                    msg = f"Bounty Contribution for Hero Faction {factionName} of {bounty} credits."
                    ret.append(Status(1, msg, CAT_BOUNTY, bounty))
                elif self.isTargetFactionName(factionName):
                    msg = f"Bounty Contribution for Enemy Faction {factionName} of {bounty} credits."
                    ret.append(Status(-1, msg, CAT_BOUNTY, bounty))
                else:
                    msg = f"Bounty Contribution for Competitor Faction {factionName} of {bounty} credits."
                    ret.append(Status(-1, msg, CAT_BOUNTY, bounty))
        return ret

    def checkCartography(self, entry: Dict) -> List[Status]:
        ret: List[Status] = []
        if self.currentlyInTargetSystem():
            factionName = self.currentStationFaction
            if factionName is not None:
                earnings = entry['TotalEarnings']
                if self.isHeroFactionName(factionName):
                    msg = f"Cartography Contribution for Hero Faction {factionName} of {earnings} credits."
                    ret.append(Status(1, msg, CAT_CARTOGRAPHY, earnings))
                elif self.isTargetFactionName(factionName):
                    msg = f"Cartography Contribution for Enemy Faction {factionName} of {earnings} credits."
                    ret.append(Status(-1, msg, CAT_CARTOGRAPHY, earnings))
                else:
                    msg = f"Cartography Contribution for Competitor Faction {factionName} of {earnings} credits."
                    ret.append(Status(-1, msg, CAT_CARTOGRAPHY, earnings))
        return ret

    def checkTrade(self, entry: Dict) -> List[Status]:
        ret: List[Status] = []
        if self.currentlyInTargetSystem():
            factionName = self.currentStationFaction
            if factionName is not None:
                cost = entry['Count'] * entry['AvgPricePaid']
                profit: int = entry['TotalSale'] - cost
                if profit > 0:
                    if self.isHeroFactionName(factionName):
                        msg = f"Positive Trade Contribution for Hero Faction {factionName} of {profit} credits."
                        ret.append(Status(1, msg, CAT_TRADE_PROFIT, profit))
                    elif self.isTargetFactionName(factionName):
                        msg = f"Positive Trade Contribution for Enemy Faction {factionName} of {profit} credits."
                        ret.append(Status(-1, msg, CAT_TRADE_PROFIT, profit))
                    else:
                        msg = f"Positive Trade Contribution for Competitor Faction {factionName} of {profit} credits."
                        ret.append(Status(-1, msg, CAT_TRADE_PROFIT, profit))
                else:
                    if self.isTargetFactionName(factionName):
                        msg = f"Negative Trade Contribution against Enemy Faction {factionName} of {profit} credits."
                        ret.append(Status(1, msg, CAT_TRADE_LOSS, profit))
                    elif self.isHeroFactionName(factionName):
                        msg = f"Negative Trade Contribution against Hero Faction {factionName} of {profit} credits."
                        ret.append(Status(-1, msg, CAT_TRADE_LOSS, profit))
                    else:
                        msg = f"Negative Trade Contribution against Competitor Faction {factionName} of {profit} credits."
                        ret.append(Status(-1, msg, CAT_TRADE_LOSS, profit))

        return ret

    def checkMissionFail(self, event: Dict) -> List[Status]:
        ret: List[Status] = []
        a = 4
        #
        # If attacks enemy faction in goal system
        #
        if a == 0:
            ret.append(Status(1, "Failed Mission against Enemy Faction", CAT_MISSION_FAIL, 1))

        #
        # If benefits hero faction in goal system
        #
        if a == 0:
            ret.append(Status(-1, "Failed Mission against Hero Faction", CAT_MISSION_FAIL, 1))

        #
        # If benefits competitor faction in goal system
        #
        if a == 0:
            ret.append(Status(-1, "Failed Mission against Neutral Faction", CAT_MISSION_FAIL, 1))

        return ret

    def checkMurder(self, event: Dict) -> List[Status]:
        ret: List[Status] = []
        a = 4
        #
        # If attacks enemy faction in goal system
        #
        if a == 0:
            ret.append(Status(1, "Murder against Enemy Faction", CAT_MURDER, 1))

        #
        # If attacks hero faction in goal system
        #
        if a == 0:
            ret.append(Status(-1, "Murder against Hero Faction", CAT_MURDER, 1))

        #
        # If attacks neutral faction in goal system
        #
        if a == 0:
            ret.append(Status(-1, "Murder against Neutral Faction", CAT_MURDER, 1))

        return ret