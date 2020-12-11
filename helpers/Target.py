# { "timestamp":"2020-11-12T22:09:36Z", "event":"ShipTargeted", "TargetLocked":true,
# "Ship":"python", "ScanStage":3, "PilotName":"$ShipName_Police_Federation;",
# "PilotName_Localised":"Federal Security Service", "PilotRank":"Competent",
# "ShieldHealth":100.000000, "HullHealth":100.000000,
# "Faction":"Pleiades Resource Enterprise", "LegalStatus":"Clean" }

class Target:
    ship: str = "Unknown"
    name: str = "Unknown"
    rank: str = "Unknown"
    faction: str = "Unknown"

    def __init__(self, name:str, faction:str, ship:str="Unknown", rank:str="Unknown"):
        self.ship = ship
        self.faction = faction
        self.ship = ship
        self.rank = rank

    def getFaction(self) -> str:
        return self.faction

    def getShip(self) -> str:
        return self.ship

    def getName(self) -> str:
        return self.name

    def getRank(self) -> str:
        return self.rank