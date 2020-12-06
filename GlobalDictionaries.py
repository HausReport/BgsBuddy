import inspect
import json
import logging
import os
from typing import Dict
try:
    from config import appname
except ImportError:
    appname = "bgsBuddy"

global_system_address_to_name: Dict[str,str] = {}
global_system_name_to_address: Dict[str,str] = {}

# Npc name, faction name
global_target_factions : Dict[str,str] = {}
try:
    plugin_name
except NameError:
    plugin_name = os.path.basename(os.path.dirname(__file__))

def getDataFilePath(fName: str) -> str:
    cwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    cwd = os.path.join(cwd,fName)
    cwd = os.path.abspath(cwd)
    return cwd

def load_addresses():
    global global_system_address_to_name
    global global_system_name_to_address

    cwd = getDataFilePath('addresses.jsonl')
    logger.info(f"Loading addresses from directory {cwd}")
    with open(cwd) as f:
        data = json.load(f)

    #logger.info(data)
    global_system_name_to_address = {k: str(v) for k, v in data}
    global_system_address_to_name = {str(v): k for k, v in data}

def saveLocalDictionary(dictionary: Dict, fName: str):
    cwd = getDataFilePath(fName)
    with open(cwd, 'w') as fp:
        json.dump(dictionary, fp)

# A Logger is used per 'found' plugin to make it easy to include the plugin's
# folder name in the logging output format.
# NB: plugin_name here *must* be the plugin's folder name as per the preceding
#     code, else the logger won't be properly set up.

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

def add_system_and_address(sys: str, add: str):
    global global_system_address_to_name
    global global_system_name_to_address
    global_system_address_to_name[add] = sys
    global_system_name_to_address[sys] = add
    sz = len(global_system_address_to_name)
    logger.info(f"Adding sys={sys}, add={add}, nitems={sz}")
    print(json.dumps(global_system_address_to_name))


def get_system_by_address(add: str) -> str:
    global global_system_address_to_name
    ret:str = global_system_address_to_name.get(add)
    sz = len(global_system_address_to_name)

    logger.info(f"Finding sys={ret}, add={add}, nitems={sz}")
    print(json.dumps(global_system_address_to_name))
    return ret


def get_address_by_system(sys: str):
    global global_system_name_to_address

    return global_system_name_to_address.get(sys)

def add_target_faction(targ: str, fac:str):
    global global_target_factions
    logger.info("Adding target to global dict")
    global_target_factions[targ] =  fac

def get_target_faction(targ: str):
    global global_target_factions

    return global_target_factions[targ]

def clear_target_dictionary():
    global global_target_factions
    global_target_factions.clear()
