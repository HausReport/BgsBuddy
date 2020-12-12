import json
from typing import List, Dict

from .DailyPlan import DailyPlan
from .LogReporter import LogReporter
from .Status import Status
from .Reporter import Reporter

#
# For timestamping
#
# from datetime import datetime
#
# timestamp = 1545730073
# dt_object = datetime.fromtimestamp(timestamp)
#
# print("dt_object =", dt_object)

#
# To add:
#
# Timestamp
# Overview
# Notes

class DailyPlans:

    def __init__(self):

        self.plans: List[DailyPlan] = []
        self.reporters: List[Reporter] = []
        # self.reporters: List[Reporter] = .append(reporter)

    def addPlan(self, plan: DailyPlan):
        self.plans.append(plan)

    def addReporter(self, reporter: Reporter):
        self.reporters.append(reporter)

    def size(self):
        return len(self.plans)

    #
    # Updated by DailyPlans as ship moves
    #
    def setCurrentSystem(self, sys: str):
        for plan in self.plans:
            plan.setCurrentSystem(sys)

    def setCurrentSystemFactions(self, factions: List[str]):
        for plan in self.plans:
            plan.setCurrentSystemFactions(factions)

    def setCurrentStation(self, sta: str):
        for plan in self.plans:
            plan.setCurrentStation(sta)

    def setCurrentStationFaction(self, fac: str):
        for plan in self.plans:
            plan.setCurrentStationFaction(fac)

    #
    # Checks against each of the plans in the list
    #
    def checkMissionSuccess(self, event: Dict):
        for plan in self.plans:
            ret = plan.checkMissionSuccess(event)
            self.report(ret, plan, event)

    def checkBounty(self, event: Dict):
        for plan in self.plans:
            ret = plan.checkBounty(event)
            self.report(ret, plan, event)

    def checkCartography(self, event: Dict):
        for plan in self.plans:
            ret = plan.checkCartography(event)
            self.report(ret, plan, event)

    def checkTrade(self, event: Dict):
        for plan in self.plans:
            ret = plan.checkTrade(event)
            self.report(ret, plan, event)

    def checkMissionFail(self, event: Dict):
        for plan in self.plans:
            ret = plan.checkMissionFail(event)
            self.report(ret, plan, event)

    def checkMurder(self, event: Dict):
        for plan in self.plans:
            ret = plan.checkMurder(event)
            self.report(ret, plan, event)

    def checkBond(self, event: Dict):
        for plan in self.plans:
            ret = plan.checkBond(event)
            self.report(ret, plan, event)

    def sendMessage(self, event: Dict, text):
        for plan in self.plans:
            ret = plan.sendMessage(event, text)
            self.report(ret, plan, event)


    def report(self, retList: List[Status], plan: DailyPlan, event: Dict):
        for ret in retList:
            for reporter in self.reporters:
                reporter.report(ret, plan, event)

    def setCommanderName(self, cmdr):
        for reporter in self.reporters:
            reporter.setCommanderName(cmdr)

    #
    # Marshalling/unmarshalling of plans as JSON(L)
    #
    def reprJSON(self):
        ret = "[\n"
        first: bool = True
        for dp in self.plans:
            if not first:
                ret = ret + ",\n"
            first = False
            ret = ret + dp.reprJSON()
        ret = ret + "\n]"
        return ret

        #             d['plans'].append(dp.reprJSON())
        # d = dict()
        # d['plans']: List[DailyPlan] = []
        # for a, v in self.__dict__.items():
        #     if a == "plans":
        #         for dp in self.plans:
        #             d['plans'].append(dp.reprJSON())
        #     elif a == "reporters":
        #         continue
        #     elif (hasattr(v, "reprJSON")):
        #         d[a] = v.reprJSON()
        #     else:
        #         d[a] = v
        # return json.dumps(d, indent=4)

    def __eq__(self, other):
        if type(other) is type(self):
            if other.size() != self.size():
                return False
            for plan in self.plans:
                if plan not in other.plans:
                    return False
            return True
        return False

