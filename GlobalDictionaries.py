import logging
import os
from typing import Dict
from config import appname

global_system_address_to_name: Dict[str,str] = {}
global_system_name_to_address: Dict[str,str] = {}

# Npc name, faction name
global_target_factions : Dict[str,str] = {}

logger = None

def add_system_and_address(sys: str, add: str):
    global global_system_address_to_name
    global global_system_name_to_address

    global_system_address_to_name[add] = sys
    global_system_name_to_address[sys] = add


def get_system_by_address(add: str) -> str:
    global global_system_address_to_name

    return global_system_address_to_name.get(add)


def get_address_by_system(sys: str):
    global global_system_name_to_address

    return global_system_name_to_address.get(sys)

def add_target_faction(targ: str, fac:str):
    global global_target_factions

    global_target_factions[targ] =  fac

def get_target_faction(targ: str):
    global global_target_factions

    return global_target_factions[targ]



try:
    plugin_name
except NameError:
    plugin_name = os.path.basename(os.path.dirname(__file__))

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

