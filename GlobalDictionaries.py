from typing import Dict

global_system_address_to_name: Dict[str,str] = {}
global_system_name_to_address: Dict[str,str] = {}

# Npc name, faction name
global_target_factions : Dict[str,str] = {}


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