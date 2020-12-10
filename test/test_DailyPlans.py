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
        samplePlan: DailyPlan = DailyPlan("Kipsigines", "Alliance of CD-33 8748", "Hodack Prison Colony")
        samplePlan.addMissionInfluenceGoal(60)
        samplePlan.addBountyGoal(16000000)
        samplePlan.addCartographyGoal(8000000)
        samplePlan.addTradeProfitGoal(8000000)
        samplePlan.addMurderGoal(6)
        samplePlan.addHookUrl(
            "https://discordapp.com/api/webhooks/785936080091873310/h43X5LxjVA6a0RQjImXKTofRs7vdu_phRNYihoblsSquVZeGJslbcou0L-zYphrpANR-")

        samplePlan2: DailyPlan = DailyPlan("HR 5975", "Beyond Infinity Corporation", "Wreaken Construction")
        samplePlan2.addMissionInfluenceGoal(60)
        samplePlan2.addBountyGoal(16000000)
        samplePlan2.addCartographyGoal(8000000)
        samplePlan2.addTradeProfitGoal(16000000)
        samplePlan2.addMurderGoal(12)
        samplePlan2.addHookUrl(
            "https://discordapp.com/api/webhooks/785361212367831041/dPSrZRbPKpPDG9QIEOf7klmw8S56rS-AiWcj8-3pB1FsiKOFLQv7j9gJDy5XK3eP34Jz")

        samplePlan3: DailyPlan = DailyPlan("LAWD 26", "Minutemen", "Sirius Corporation")
        samplePlan3.addMissionInfluenceGoal(90)
        samplePlan3.addBountyGoal(16000000)
        samplePlan3.addCartographyGoal(8000000)
        samplePlan3.addTradeProfitGoal(0)
        samplePlan3.addTradeLossGoal(16000000)
        samplePlan3.addMurderGoal(32)
        samplePlan3.addHookUrl(
            "https://discordapp.com/api/webhooks/785228043128012820/uFmUix9PqWhh1cAoYYx1Hsh43VVmGPwCnNQlq5is1vBhqKUTeC2h0-VgDXfmQttuq9UX")

        samplePlan4: DailyPlan = DailyPlan("Solati", "Alliance of CD-33 8748", "Hodack Prison Colony")
        samplePlan4.addMissionInfluenceGoal(60)
        samplePlan4.addBountyGoal(16000000)
        samplePlan4.addCartographyGoal(8000000)
        samplePlan4.addTradeProfitGoal(16000000)
        samplePlan4.addMurderGoal(6)
        samplePlan4.addHookUrl(
            "https://discordapp.com/api/webhooks/785936584716976158/3qQG9ovZB4_PPx7np9tIHXZXeBIq0OcvXFu0vMsD7RKGixYs1_xd-fHn9fLrVZiiOq9R")
        samplePlan4.addBlightGoal(1)
        samplePlan4.addOutbreakGoal(2)
        samplePlan4.addTerrorismGoal(3)
        samplePlan4.addNaturalDisasterGoal(4)
        samplePlan4.addFamineGoal(5)
        samplePlan4.addDraughtGoal(6)
        samplePlan4.addInfrastructureFailureGoal(7)

        self.dailyPlans: DailyPlans = DailyPlans()
        self.dailyPlans.addReporter(logReporter)
        self.dailyPlans.addPlan(samplePlan)
        self.dailyPlans.addPlan(samplePlan2)
        self.dailyPlans.addPlan(samplePlan3)
        self.dailyPlans.addPlan(samplePlan4)
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

    # def test_download_plan(self):
    #     dp = IoHelpers.downloadDailyPlans("TestDailyPlans.json")
    #     print("AFTER DOWNLOADING")
    #     print("==================================================")
    #     print(dp.reprJSON())
    #     assert dp == self.dailyPlans



