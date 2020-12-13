#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
from pprint import pprint
from unittest import TestCase

import GlobalDictionaries
from helpers.DailyPlan import DailyPlan


class TestDailyPlan(TestCase):
    def setUp(self):
        GlobalDictionaries.init_logger()
        self.samplePlan: DailyPlan = DailyPlan("LHS 2477", "Federal Reclamation Co", "Hodack Prison Colony")
        self.samplePlan.addMissionInfluenceGoal(60)
        self.samplePlan.addBountyGoal(16000000)
        self.samplePlan.addCartographyGoal(8000000)
        self.samplePlan.addTradeProfitGoal(16000000)
        self.samplePlan.addHookUrl(
        "https://discordapp.com/api/webhooks/785361212367831041/dPSrZRbPKpPDG9QIEOf7klmw8S56rS-AiWcj8-3pB1FsiKOFLQv7j9gJDy5XK3eP34Jz")
        self.samplePlan.addHookUrl(
        "https://discordapp.com/api/webhooks/785228043128012820/uFmUix9PqWhh1cAoYYx1Hsh43VVmGPwCnNQlq5is1vBhqKUTeC2h0-VgDXfmQttuq9UX")

    def tearDown(self):
        pass

    def test_to_dict(self):
        dv = self.samplePlan.reprJSON()
        print("--->" + dv + "<----")
        #pprint(dv)

    def test_to_string(self):
        ret = self.samplePlan.toString()
        print(ret)
