from typing import Set, List

badGuys: Set[str] = {'Abroin Universal PLC',
                     'Aegis Core', 'Aegis Defense', 'Aegis Research',
                     'Bill Turner',
                     'CQC Holdings',
                     'Gallant Investment Brokers', 'Hodack Prison Colony',
                     'Janus Incorporated', "Namarii Emperor's Dawn",
                     'Pleiades Resource Enterprise',
                     'Reyan BPS', 'Reynhardt IntelliSys',
                     'Sirius Atmospherics', 'Sirius Catering', 'Sirius Corporation',
                     'Sirius Drives', 'Sirius Hot2Cold', 'Sirius Hyperspace',
                     'Sirius Industrial', 'Sirius Luxury Transports', 'Sirius Mining Merope',
                     'Sirius Mining', 'Sirius Power',
                     'The Greenventure Group',
                     'The Peterson Group', 'The Rockforth Corporation',
                     'Turner Research Group', 'Wiggins Development Trust',
                     'Wreaken Construction'
                        }
badGuysLower: Set[str] = {}
for string in badGuys:
    badGuysLower.add(string.lower())

def isBadGuy(name: str) -> bool:
    lName = name.lower()
    return lName in badGuysLower

def hasBadGuy(names: List[str]) -> bool:
    for name in names:
        if isBadGuy(name):
            return True
    return False