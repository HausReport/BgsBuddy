#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
from abc import ABC, abstractmethod
from typing import Dict

from .DailyPlan import DailyPlan
from .Status import Status

class Reporter(ABC):

    @abstractmethod
    def report(self, ret: Status, plan: DailyPlan, event: Dict):
        pass
