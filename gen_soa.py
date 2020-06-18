import os
import sys
import argparse
from fractions import Fraction
from typing import List, Tuple, Dict, Set
from random import sample, choice, randint
from soadata import DataSystem

if not (sys.version_info.major == 3 and sys.version_info.minor >= 5):
    print("This script requires Python 3.5 or higher!")
    print("You are using Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))
    sys.exit(1)

parser = argparse.ArgumentParser(description = 'Generates a simulation for service oriented architecture')
parser.add_argument("-y", "--system", help="the number of data systems", required = True)
parser.add_argument("-d", "--datatypes", help="the number of datatypes", required = True)
parser.add_argument("-c", "--classes", help="the number of data classes", required = True)
parser.add_argument("-s", "--services", help="the number of data services", required = True)
parser.add_argument("-rc", "--refclassratio", help="ratio of class with ref vs simple POJO", default = "1/10")
parser.add_argument("-rs", "--refserviceratio", help="ratio of services with ref vs simple POJO", default = "1/2")
parser.add_argument("-p", "--properties", help="the max number of properties per class", required = True)
parser.add_argument("-n", "--names", help="the number of property names", default = "200")
parser.add_argument("-r", "--refratio", help="ratio of ref vs simple types", default = "1/10")
args = parser.parse_args()

MAX_ITEMS_MAGNITUDE = 48 #2^48
MAX_PROCESSING_MAGNITUDE_MICRO_SEC = 27 # 2^27
ROOT_PROCESSING_MAGNITUDE_MICRO_SEC = 10 # ms
WORSE_ERROR_RATE = 2
ROOT_ERROR_RATE = 6

class Config:
    def __init__(self):
        self.datasystem_count = int(args.system)
        self.datatype_count = int(args.datatypes)
        self.class_count = int(args.classes)
        self.properties_max = int(args.properties)
        self.property_name_count = int(args.names)
        self.ref_ratio = Fraction(args.refratio)
        self.ref_class_ratio = Fraction(args.refclassratio)
        self.service_count = int(args.services)
        self.ref_service_ratio = Fraction(args.refserviceratio)
    
    def get_ref_class_count(self)->int:
        return int(self.class_count * self.ref_class_ratio)
    
    def get_simple_class_count(self)->int:
        return self.class_count - self.get_ref_class_count()

    def get_ref_service_count(self)->int:
        return int(self.service_count * self.ref_service_ratio)
    
    def get_simple_service_count(self)->int:
        return self.service_count - self.get_ref_service_count()

config = Config()

for _ in range(config.datatype_count):
    dataSystem = DataSystem()
    dataSystem.add_n_datatypes(config.datatype_count)
    dataSystem.add_n_property_names(config.property_name_count)
    dataSystem.add_simple_dataclass_auto(class_count = config.get_simple_class_count(), max_property = config.properties_max, max_items = MAX_ITEMS_MAGNITUDE)
    dataSystem.add_basic_dataservice_auto(service_count = config.service_count, max_proc_micro_sec = MAX_PROCESSING_MAGNITUDE_MICRO_SEC, worse_error_rate=WORSE_ERROR_RATE)
    dataSystem.set_root_service(proc_micro_sec=ROOT_PROCESSING_MAGNITUDE_MICRO_SEC, err_proc_micro_sec=ROOT_PROCESSING_MAGNITUDE_MICRO_SEC, worse_error_rate=ROOT_ERROR_RATE)
    print(dataSystem)
