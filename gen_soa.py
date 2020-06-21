import os
import sys
import argparse
import json
from fractions import Fraction
from typing import List, Tuple, Dict, Set
from random import sample, choice, randint
from soadata import DataSystem, DataSystemConfig

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

dataconfig = DataSystemConfig.from_obj(load_config())
print(dataconfig)

for _ in range(dataconfig.datasystem_count):
    dataSystem = DataSystem(dataconfig)
    dataSystem.prepare()
    print(dataSystem)
