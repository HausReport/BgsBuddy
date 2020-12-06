from pprint import pprint
from unittest import TestCase

from craid.bgsBuddy import GlobalDictionaries
from craid.bgsBuddy.helpers.DailyPlan import DailyPlan
from craid.bgsBuddy.helpers.DailyPlans import DailyPlans
from craid.bgsBuddy.helpers.DiscordReporter import DiscordReporter
from craid.bgsBuddy.helpers.LogReporter import LogReporter


class TestDailyPlans(TestCase):
    # def __init__(self, name, module):
    #     super().__init__(name, module)
    #     print("Hi!")

    def setUp(self):
        GlobalDictionaries.init_logger()
        logger = GlobalDictionaries.logger

        logReporter: LogReporter = LogReporter(logger)

        samplePlan: DailyPlan = DailyPlan("LHS 2477", "Federal Reclamation Co", "Hodack Prison Colony")
        samplePlan.addMissionInfluenceGoal(60)
        samplePlan.addBountyGoal(16000000)
        samplePlan.addCartographyGoal(8000000)
        samplePlan.addTradeProfitGoal(16000000)

        samplePlan2: DailyPlan = DailyPlan("HR 5975", "Beyond Infinity Corporation", "Wreaken Construction")
        samplePlan2.addMissionInfluenceGoal(60)
        samplePlan2.addBountyGoal(16000000)
        samplePlan2.addCartographyGoal(8000000)
        samplePlan2.addTradeProfitGoal(16000000)

        self.dailyPlans: DailyPlans = DailyPlans(logReporter)
        self.dailyPlans.addPlan(samplePlan)
        self.dailyPlans.addPlan(samplePlan2)
        disco = DiscordReporter(logger)
        self.dailyPlans.addReporter(disco)

    def tearDown(self):
        pass

    def test_add_plan(self):
        dv = self.dailyPlans.to_dict()
        pprint(dv)
