import inspect
import json
import logging
import os
from typing import Dict, List

from helpers.Target import Target

try:
    from config import appname
except ImportError:
    appname = "bgsBuddy"

# test
# Npc name, faction name
global_target_factions: Dict[str, Target] = {}
try:
    plugin_name
except NameError:
    plugin_name = os.path.basename(os.path.dirname(__file__))

#
# Dictionary/JSON file I/O
#
def getDataFilePath(fName: str) -> str:
    cwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    cwd = os.path.join(cwd, fName)
    cwd = os.path.abspath(cwd)
    return cwd


cwd = getDataFilePath('addresses.jsonl')
with open(cwd) as f:
    data: Dict[str, str] = json.load(f)

dlen = len(data)
# logger.info(f"{dlen} items loaded in dict")

global_system_address_to_name: Dict[str, str] = {}
global_system_name_to_address: Dict[str, str] = {}

for k in data.keys():
    key = str(k)
    val = str(data[key])
    global_system_name_to_address[key] = val
    global_system_address_to_name[val] = key


#
# Global logger
#

def init_logger():
    global logger
    logger_name = f'{appname}.{plugin_name}'
    logger = logging.getLogger(logger_name)
    # If the Logger has handlers then it was already set up by the core code, else
    # it needs setting up here.
    if not logger.hasHandlers():
        level = logging.INFO  # So logger.info(...) is equivalent to print()

        logger.setLevel(level)
        logger_channel = logging.StreamHandler()
        logger_formatter = logging.Formatter(
            f'%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d:%(funcName)s: %(message)s')
        logger_formatter.default_time_format = '%Y-%m-%d %H:%M:%S'
        logger_formatter.default_msec_format = '%s.%03d'
        logger_channel.setFormatter(logger_formatter)
        logger.addHandler(logger_channel)


def saveLocalDictionary(dictionary: Dict, fName: str):
    global logger
    cwd = getDataFilePath(fName)
    with open(cwd, 'w') as fp:
        json.dump(dictionary, fp)
    logger.info(f"Saved dict to >{cwd}<")

#
# Sometimes star systems are identified by their name, other times by their address.
# This (imperfectly) correlates the two.  There are a few star systems with identical names.
# There are probably star systems that are identified by two different names (eg Delphi).
#
def add_system_and_address(sys: str, add: str):
    global global_system_address_to_name
    global global_system_name_to_address

    if sys not in global_system_name_to_address:
        global_system_address_to_name[add] = sys
        global_system_name_to_address[sys] = add
        sz = len(global_system_address_to_name)
        logger.info(f"Adding sys={sys}, add={add}, nitems={sz} and saving addresses.jsonl")
        saveLocalDictionary(global_system_name_to_address, "addresses.jsonl")
        # print(json.dumps(global_system_address_to_name))


def get_system_by_address(add: str) -> str:
    global global_system_address_to_name
    ret: str = global_system_address_to_name.get(add)
    sz = len(global_system_address_to_name)

    logger.info(f"Finding sys={ret}, add={add}, nitems={sz}")
    return ret


def get_address_by_system(sys: str):
    global global_system_name_to_address

    return global_system_name_to_address.get(sys)


#
# Keeps track of information about targeted ships
#
ship_types: Dict[str, str] = {
    "adder"                   : "Adder",
    "anaconda"                : "Anaconda",
    "asp"                     : "Asp",
    "asp_scout"               : "Asp Scout",
    "belugaliner"             : "Beluga Liner",
    "cobramkiii"              : "Cobra Mk III",
    "cobramkiv"               : "Cobra Mk IV",
    "cutter"                  : "Imperial Cutter",
    "diamondback"             : "Diamondback Scout",
    "diamondbackxl"           : "Diamondback Explorer",
    "dolphin"                 : "Dolphin",
    "eagle"                   : "Eagle",
    "empire_courier"          : "Imperial Courier",
    "empire_eagle"            : "Imperial Eagle",
    "empire_fighter"          : "Imperial Fighter",
    "empire_trader"           : "Imperial Trader",
    "federation_corvette"     : "Federal Corvette",
    "federation_dropship"     : "Federal Dropship",
    "federation_dropship_mkii": "Federal Dropship Mk II",
    "federation_fighter"      : "Federal Fighter",
    "federation_gunship"      : "Federal Gunship",
    "ferdelance"              : "Fer-de-Lance",
    "gdn_hybrid_fighter_v1"   : "Guardian Hybrid Fighter V1",
    "gdn_hybrid_fighter_v3"   : "Guardian Hybrid Fighter V2",
    "hauler"                  : "Hauler",
    "independant_trader"      : "Independent Trader",
    "independent_fighter"     : "Independent Fighter",
    "krait_light"             : "Krait Light",
    "krait_mkii"              : "Krait Mk II",
    "mamba"                   : "Mamba",
    "orca"                    : "Orca",
    "python"                  : "Python",
    "sidewinder"              : "Sidewinder",
    "type6"                   : "Type-6 Transporter",
    "type7"                   : "Type-7 Transporter",
    "type9"                   : "Type-9 Heavy",
    "type9_military"          : "Type-9 Military",
    "typex"                   : "Type 10 Defender",
    "typex_2"                 : "Type 10 Defender (mod 2)",
    "typex_3"                 : "Type 10 Defender (mod 3)",
    "viper"                   : "Viper",
    "viper_mkiv"              : "Viper Mk IV",
    "vulture"                 : "Vulture"}


def add_target_faction(name: str, targ: Target):
    global global_target_factions
    logger.info("Adding target to global dict")
    global_target_factions[name] = targ


def get_target_faction(name: str):
    global global_target_factions

    if name in global_target_factions:
        targ: Target = global_target_factions[name]
        return targ.getFaction()

    return None  # "Unknown Faction"


def get_target_string(name: str):
    global global_target_factions
    ret = "Unknown Target"

    if name in global_target_factions:
        targ: Target = global_target_factions[name]
        ship_name = get_ship_name(targ.ship)
        ret = f"( {ship_name}, {targ.rank})"

    return ret


def clear_target_dictionary():
    global global_target_factions
    global_target_factions.clear()


def get_ship_name(name: str):
    global ship_types

    if name in ship_types:
        return ship_types[name]

    return name
