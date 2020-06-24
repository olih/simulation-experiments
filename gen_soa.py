import os
import sys
import argparse
import json
from fractions import Fraction
from typing import List, Tuple, Dict, Set
from random import sample, choice, randint
from soadata import DataSystem, DataSystemConfig, ServiceCost

if not (sys.version_info.major == 3 and sys.version_info.minor >= 5):
    print("This script requires Python 3.5 or higher!")
    print("You are using Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))
    sys.exit(1)

parser = argparse.ArgumentParser(description = 'Generates a simulation for service oriented architecture')
parser.add_argument("-c", "--configfile", help="the json configuration file", required = True)
args = parser.parse_args()

MAX_ITEMS_MAGNITUDE = 48 #2^48
MAX_PROCESSING_MAGNITUDE_MICRO_SEC = 27 # 2^27

class ScriptConfig:
    def __init__(self):
        self.config_file = args.configfile

scriptconfig = ScriptConfig()

def load_config():
    with open(scriptconfig.config_file, 'r') as jsonfile:
        return json.load(jsonfile)

wholeconfig = load_config()
dataconfig = DataSystemConfig.from_obj(wholeconfig["experiment"])
print(dataconfig)

serviceCost = ServiceCost.from_obj(wholeconfig["calculator"]["cost"])

for _ in range(dataconfig.datasystem_count):
    dataSystem = DataSystem(dataconfig)
    dataSystem.prepare()
    print("\n\n>>>>",dataSystem.get_used_ref_datatypes())
    # print(dataSystem.get_ref_types())
    exit()
    services = dataSystem.get_services()
    costs = [(service.name, serviceCost.get_cost(service)) for service in services]
    dataclasses = dataSystem.get_dataclasses()
    for dataclass in dataclasses:
        print("name: {}, weight: {}".format(dataclass.name, dataclass.get_weight()))
