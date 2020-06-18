import os
import sys
import argparse
from typing import List, Tuple, Dict, Set
from soadata import DataPropertyTypeRepo, DataPropertyNameRepo

if not (sys.version_info.major == 3 and sys.version_info.minor >= 5):
    print("This script requires Python 3.5 or higher!")
    print("You are using Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))
    sys.exit(1)

parser = argparse.ArgumentParser(description = 'Generates a simulation for service oriented architecture')
parser.add_argument("-d", "--datatypes", help="the number of datatypes", required = True)
parser.add_argument("-n", "--names", help="the number of property names", default = 200)
args = parser.parse_args()

dataPropertyTypeRepo = DataPropertyTypeRepo()
dataPropertyTypeRepo.add_types_as_str("Bool Int Float DateTime")
dataPropertyTypeRepo.add_types(["Type{}".format(i) for i in range(int(args.datatypes))])

dataPropertyNameRepo = DataPropertyNameRepo()
dataPropertyNameRepo.add_names_auto(args.names)

print(dataPropertyTypeRepo)
print(dataPropertyNameRepo)