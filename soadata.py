from fractions import Fraction
from typing import List, Tuple, Set
from enum import Enum, auto
from random import sample, choice, randint

class DataPropertyType:
    def __init__(self, datatype: str):
        self.datatype = datatype
    
    @classmethod
    def from_ref_datatype(cls, servicename: str, dataname: str):
        return cls(servicename + ":" + dataname)
    
    def to_string(self):
        return self.datatype

    def __str__(self):
        return self.to_string()
    
    def __repr__(self):
        return self.to_string()
    
    def __eq__(self, other):
        return self.datatype == other.datatype

    def __hash__(self):
        return hash(self.datatype)
    
    def is_ref(self)->bool:
        return ":" in self.datatype

intDataPropertyType= DataPropertyType("Int")

class DataProperty:
    """A property
    Example: colors : Int[3, 3] """
    def __init__(self):
        self.name = ""
        self.datatype = intDataPropertyType
        self.min_items = 0
        self.max_items = 1
    
    def set_name(self, name: str):
        self.name = name
        return self
    
    def set_datatype(self, datatype: DataPropertyType):
        self.datatype = datatype
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
    
    def add(self, prop: DataProperty):
        self.properties.add(prop)
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
        self.processing_magnitude = 1
        self.error_processing_magnitude = 1
        self.error_rate = Fraction(1,1000000)

    def set_name(self, name: str):
        self.name = name
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
        return "Service {}: processing_magnitude = {}, error_processing_magnitude = {}, error_rate = {}".format(self.name, self.processing_magnitude, self.error_processing_magnitude, self.error_rate)
    
    def __str__(self):
        return self.to_string()
    
    def __repr__(self):
        return self.to_string()

    def __eq__(self, other):
        return (self.name, self.processing_magnitude) == (other.name, other.processing_magnitude)
 
    def __hash__(self):
        return hash((self.name, self.processing_magnitude))

    def rand_error_rate(self)->bool:
        """ Return true if the error rate has been triggered"""
        alea = randint(1, self.error_rate.denominator)
        return alea <= self.error_rate.numerator

class DataPropertyTypeRepo:
    def __init__(self):
        self.simple_store = set([])
        self.ref_store = set([])
    
    def add(self, dataPropertyType: DataPropertyType):
        if (dataPropertyType.is_ref()):
            self.ref_store.add(dataPropertyType)
        else:
            self.simple_store.add(dataPropertyType)
        return self
    
    def discard(self, dataPropertyType: DataPropertyType):
        if (dataPropertyType.is_ref()):
            self.ref_store.discard(dataPropertyType)
        else:
            self.simple_store.discard(dataPropertyType)
        return self
    
    def __len__(self):
        return len(self.simple_store) + len(self.ref_store)

    def __str__(self):
        return "DataPropertyTypeRepo: size {}".format(len(self))

    def has(self, dataPropertyType: DataPropertyType)->bool:
        return dataPropertyType in self.simple_store or dataPropertyType in self.ref_store

    def add_types(self, types: List[str]):
        for t in types:
            self.add(DataPropertyType(t))
        return self

    def add_types_as_str(self, types: str):
        return self.add_types(types.split(" "))

    def simple_types_as_list(self):
        return list(self.simple_store)

    def random_simple_type(self)->DataPropertyType:
        return choice(self.simple_types_as_list())

    def ref_types_as_list(self):
        return list(self.ref_store)

    def random_ref_type(self)->DataPropertyType:
        return choice(self.ref_types_as_list())

    def random_type(self, refRatio: Fraction)->DataPropertyType:
        alea = randint(1, refRatio.denominator)
        isRef = alea <= refRatio.numerator
        return self.random_ref_type() if isRef else self.random_simple_type()

class DataPropertyNameRepo:
    """ These are usually human readable and are re-used across classes but not necessarily in a consistent manner. Ex: name, description, ... """
    def __init__(self):
        self.counter = 0
        self.names = set([])
    
    def add_name(self, name: str):
        self.names.add(name)
        return name

    def add_next_name(self):
        self.counter = self.counter + 1
        return self.add_name("Name{}".format(self.counter))

    def add_names_auto(self, count: int):
        for _ in range(count):
            self.add_next_name()
        return self

    def __len__(self):
        return len(self.names)

    def __str__(self):
        return "DataPropertyNameRepo: size {}".format(len(self))

    def has(self, name: str)->bool:
        return name in self.names

    def sample(self, count: int)->List[str]:
        return sample(list(self.names), count)

class DataClassNameRepo:
    """ These are usually human readable and are re-used across classes but not necessarily in a consistent manner. Ex: Person, ... """
    def __init__(self):
        self.counter = 0
        self.names = set([])
    
    def add_name(self, name: str):
        self.names.add(name)
        return name

    def add_next_name(self):
        self.counter = self.counter + 1
        return self.add_name("ClassName{}".format(self.counter))

    def add_names_auto(self, count: int):
        for i in range(count):
            self.add_next_name()
        return self

    def __len__(self):
        return len(self.names)

    def __str__(self):
        return "DataClassNameRepo: size {}".format(len(self))

    def has(self, name: str)->bool:
        return name in self.names

class DataClassRepo:
    """  Store a class with a list of properties """
    def __init__(self):
        self.dataclasses = {}
    
    def add_dataclass(self, dataclass: DataClass):
        self.dataclasses[dataclass.name] = dataclass
        return self

    def remove_dataclass(self, dataclass: DataClass):
        if dataclass.name in self.dataclasses:
            del self.dataclasses[dataclass.name]
        return self

    def __len__(self):
        return len(self.dataclasses)

    def __str__(self):
        return "DataClassRepo: size {}".format(len(self))

    def has(self, name: str)->bool:
        return name in self.dataclasses

    def choice(self)->DataClass:
        return self.dataclasses[choice(list(self.dataclasses.keys()))]

class DataServiceNameRepo:
    """ These could human readable and are re-used across classes but not necessarily in a consistent manner. Ex: PersonDB, ... """
    def __init__(self):
        self.counter = 0
        self.names = set([])
    
    def add_name(self, name: str):
        self.names.add(name)
        return name

    def add_next_name(self):
        self.counter = self.counter + 1
        return self.add_name("ServiceName{}".format(self.counter))

    def add_names_auto(self, count: int):
        for i in range(count):
            self.add_next_name()
        return self

    def __len__(self):
        return len(self.names)

    def __str__(self):
        return "DataServiceNameRepo: size {}".format(len(self))

    def has(self, name: str)->bool:
        return name in self.names

class DataServiceRepo:
    """  Store a service  """
    def __init__(self):
        self.dataservices = {}
    
    def add_dataservice(self, dataservice: DataService):
        self.dataservices[dataservice.name] = dataservice
        return self

    def remove_dataservice(self, dataservice: DataService):
        if dataservice.name in self.dataservices:
            del self.dataservices[dataservice.name]
        return self

    def __len__(self):
        return len(self.dataservices)

    def __str__(self):
        return "DataServiceRepo: size {}".format(len(self))

    def has(self, name: str)->bool:
        return name in self.dataservices

class DataSystem:
    def __init__(self):
        self.data_property_type_repo = DataPropertyTypeRepo()
        self.data_property_name_repo = DataPropertyNameRepo()
        self.data_class_name_repo = DataClassNameRepo()
        self.data_class_repo = DataClassRepo()
        self.data_service_name_repo = DataServiceNameRepo()
        self.data_service_repo = DataServiceRepo()
        self.root_service = DataService().set_name("root")
        
    def add_dataclass_auto(self)->DataClass:
        dataClass = DataClass()
        dataClass.set_name(self.data_class_name_repo.add_next_name())
        self.data_class_repo.add_dataclass(dataClass)
        return dataClass

    def add_dataservice_auto(self)->DataService:
        dataService = DataService()
        dataService.set_name(self.data_service_name_repo.add_next_name())
        self.data_service_repo.add_dataservice(dataService)
        return dataService

    def add_n_datatypes(self, count: int):
        self.data_property_type_repo.add_types_as_str("Bool Int Float")
        self.data_property_type_repo.add_types(["Type{}".format(i) for i in range(count)])

    def add_n_property_names(self, count: int):
        self.data_property_name_repo.add_names_auto(count)

    def add_simple_dataclass_auto(self, class_count: int, max_property: int, max_items: int):
        for _ in range(class_count):
            dataClass = self.add_dataclass_auto()
            propertyNames = self.data_property_name_repo.sample(randint(1, max_property))
            for pname in propertyNames:
                prop = DataProperty()
                prop.set_name(pname)
                prop.set_max_items(randint(1, max_items))
                prop.set_min_items(randint(0, prop.max_items))
                prop.set_datatype(self.data_property_type_repo.random_simple_type())
                dataClass.add(prop)

    def add_basic_dataservice_auto(self, service_count: int, max_proc_micro_sec: int, worse_error_rate: int = 2):
        for _ in range(service_count):
            dataService = self.add_dataservice_auto()
            dataService.set_processing_magnitude(randint(1, max_proc_micro_sec))
            dataService.set_error_processing_magnitude(randint(1, max_proc_micro_sec))
            dataService.set_error_rate(Fraction(1, 10**randint(worse_error_rate, 8)))

    def set_root_service(self, proc_micro_sec: int = 1, err_proc_micro_sec: int = 1, worse_error_rate: int = 2):
        self.root_service.set_processing_magnitude(proc_micro_sec)
        self.root_service.set_error_processing_magnitude(err_proc_micro_sec)
        self.root_service.set_error_rate(Fraction(1, 10**worse_error_rate))

    def __str__(self):
        return "DataSystem: {}, {}, {}, {}".format(self.data_property_type_repo, self.data_class_repo, self.data_service_repo, self.root_service)
