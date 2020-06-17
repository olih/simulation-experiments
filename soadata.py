from fractions import Fraction
from typing import List, Tuple, Set
from enum import Enum, auto
from random import sample, choice, randint

class DataProperty:
    """A property
    Example: colors : Int[3, 3] """
    def __init__(self):
        self.name = ""
        self.datatype = "Int"
        self.min_items = 0
        self.max_items = 1
    
    def set_name(self, name: str):
        self.name = name
        return self
    
    def set_datatype(self, datatype: str):
        self.datatype = datatype
        return self
    
    def set_ref_datatype(self, servicename: str, dataname: str):
        self.datatype = servicename + ":" + dataname
        return self

    def set_min_items(self, min_items: int):
        self.min_items = min_items
        return self

    def set_max_items(self, max_items: int):
        self.max_items = max_items
        return self

    def to_string(self):
        return "{} : {} [{}, {}]".format(self.name, self.datatype, self.min_items, self.max_items)

    def __str__(self):
        return self.to_string()
    
    def __repr__(self):
        return self.to_string()

    def __eq__(self, other):
        thisone = (self.name, self.datatype, self.min_items, self.max_items)
        otherone = (other.name, other.datatype, other.min_items, other.max_items)
        return thisone == otherone

    def __hash__(self):
        return hash((self.name, self.datatype, self.min_items, self.max_items))
    

class DataClass:
    """A data class containing a list of properties """
    def __init__(self):
        self.name = ""
        self.properties = set([])

    def set_name(self, name: str):
        self.name = name
        return self

    def set_properties(self, props: Set[DataProperty]):
        self.properties = props
        return self
    
    def to_string(self):
        return "name = {}\n----\n".format(self.name) + "/n".join([str(p) for p in self.properties])
    
    def __str__(self):
        return self.to_string()
    
    def __repr__(self):
        return self.to_string()
    
    def __eq__(self, other):
        return (self.name, self.properties) == (other.name, other.properties)
    
    def __hash__(self):
        return hash((self.name, self.properties))
    
    def __len__(self):
        return len(self.properties)

class DataService:
    """A data service attached to a service """
    def __init__(self):
        self.name = ""
        self.dataclass = None
        self.processing_magnitude = 1
        self.error_processing_magnitude = 1
        self.error_rate = Fraction(1,1000000)

    def set_name(self, name: str):
        self.name = name
        return self

    def set_dataclass(self, dataclass: DataClass):
        self.dataclass = dataclass
        return self
    
    def set_processing_magnitude(self, processing_magnitude: int):
        self.processing_magnitude = processing_magnitude
        return self

    def set_error_processing_magnitude(self, error_processing_magnitude: int):
        self.error_processing_magnitude = error_processing_magnitude
        return self

    def set_error_rate(self, error_rate: Fraction):
        self.error_rate = error_rate
        return self

    def to_string(self):
        return "service {} for class {}: processing_magnitude = {}, error_processing_magnitude = {}, error_rate = {}".format(self.name, self.dataclass.name, self.processing_magnitude, self.error_processing_magnitude, self.error_rate)
    
    def __str__(self):
        return self.to_string()
    
    def __repr__(self):
        return self.to_string()

    def __eq__(self, other):
        return (self.name, self.dataclass.name) == (other.name, other.dataclass.name)
 
    def __hash__(self):
        return hash((self.name, self.dataclass.name))

    def rand_error_rate(self)->bool:
        """ Return true if the error rate has been triggered"""
        alea = randint(1, self.error_rate.denominator)
        return alea <= self.error_rate.numerator
