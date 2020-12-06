#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

from unittest import TestCase

from craid.bgsBuddy import GlobalDictionaries


class Test(TestCase):

    def setUp(self):
        GlobalDictionaries.init_logger()
        logger = GlobalDictionaries.logger
        #GlobalDictionaries.load_addresses()

    def tearDown(self):
        pass

    def test_get_system_by_address(self):
        nam = "Aasgay"
        add = "2871051494833"
        foo = GlobalDictionaries.get_system_by_address(add)
        print(f"Returned value: {foo} expecting: {nam}")
        assert nam == foo

    def test_get_address_by_system(self):
        nam = "Aasgay"
        add = "2871051494833"
        foo = GlobalDictionaries.get_address_by_system(nam)
        print(f"Returned value: {foo} expecting: {add}")
        assert add == foo
