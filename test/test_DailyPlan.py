#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
from pprint import pprint
from unittest import TestCase

from craid.bgsBuddy import GlobalDictionaries
from craid.bgsBuddy.helpers.DailyPlan import DailyPlan


class TestDailyPlan(TestCase):
    def setUp(self):
        GlobalDictionaries.init_logger()
        self.samplePlan: DailyPlan = DailyPlan("LHS 2477", "Federal Reclamation Co", "Hodack Prison Colony")
        self.samplePlan.addMissionInfluenceGoal(60)
        self.samplePlan.addBountyGoal(16000000)
        self.samplePlan.addCartographyGoal(8000000)
        self.samplePlan.addTradeProfitGoal(16000000)


    def tearDown(self):
        pass

    def test_to_dict(self):
        dv = self.samplePlan.to_dict()
        pprint(dv)
