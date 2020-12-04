import logging
import os
from typing import Dict

from .DailyPlan import DailyPlan
from .Status import Status
from .Reporter import Reporter


class LogReporter(Reporter):

    def __init__(self, logger):
        self.logger = logger

    def report(self, ret: Status, plan: DailyPlan, event: Dict):
        if ret.type != 0:
            self.logger.info( ret.msg)
