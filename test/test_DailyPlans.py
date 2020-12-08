from pprint import pprint
from unittest import TestCase

import GlobalDictionaries
from helpers.DailyPlan import DailyPlan
from helpers.DailyPlans import DailyPlans
from helpers.DiscordReporter import DiscordReporter
from helpers.LogReporter import LogReporter
import IoHelpers

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
        samplePlan.addHookUrl(
            "https://discordapp.com/api/webhooks/785361212367831041/dPSrZRbPKpPDG9QIEOf7klmw8S56rS-AiWcj8-3pB1FsiKOFLQv7j9gJDy5XK3eP34Jz")

        samplePlan2: DailyPlan = DailyPlan("HR 5975", "Beyond Infinity Corporation", "Wreaken Construction")
        samplePlan2.addMissionInfluenceGoal(60)
        samplePlan2.addBountyGoal(16000000)
        samplePlan2.addCartographyGoal(8000000)
        samplePlan2.addTradeProfitGoal(16000000)
        samplePlan2.addHookUrl(
            "https://discordapp.com/api/webhooks/785228043128012820/uFmUix9PqWhh1cAoYYx1Hsh43VVmGPwCnNQlq5is1vBhqKUTeC2h0-VgDXfmQttuq9UX")

        self.dailyPlans: DailyPlans = DailyPlans()
        self.dailyPlans.addReporter(logReporter)
        self.dailyPlans.addPlan(samplePlan)
        self.dailyPlans.addPlan(samplePlan2)
        disco = DiscordReporter(logger)
        self.dailyPlans.addReporter(disco)

    def tearDown(self):
        pass

    def test_add_plan(self):
        dv = self.dailyPlans.reprJSON()
        print("BEFORE SAVING")
        print("==================================================")
        print(dv)
        IoHelpers.saveDailyPlans("TestDailyPlans.json", self.dailyPlans)

    def test_read_plan(self):
        dp = IoHelpers.loadDailyPlans("TestDailyPlans.json")
        print("AFTER LOADING")
        print("==================================================")
        print(dp.reprJSON())
        assert dp == self.dailyPlans
