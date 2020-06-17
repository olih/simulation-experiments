from fractions import Fraction
from typing import List, Tuple
from enum import Enum, auto
from random import sample, choice

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
    
