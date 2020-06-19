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

class DataFeature:
    """A feature that can be added to a service"""
    def __init__(self):
        self.name = ""
        self.category_name = "default"
    
    def set_name(self, name: str):
        self.name = name
        return self

    def set_category_name(self, category_name: str):
        self.category_name = category_name
        return self
    
    def to_string(self):
        return "DataFeature: {}, category: {}".format(self.name, self.category_name)
    def __str__(self):
        return self.to_string()
    
    def __repr__(self):
        return self.to_string()

    def __eq__(self, other):
        return (self.name, self.category_name) == (other.name, other.category_name)
    
    def __hash__(self):
        return hash((self.name, self.category_name))

class DataService:
    """A data service attached to a service """
    def __init__(self):
        self.name = ""
        self.processing_magnitude = 1
        self.error_processing_magnitude = 1
        self.error_rate = Fraction(1,1000000)
        self.max_memory_byte = 100000
        self.timeout_magnitude = 27
        self.features = []

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

    def set_max_memory_byte(self, max_memory_byte: int):
        self.max_memory_byte = max_memory_byte
        return self

    def set_timeout_magnitude(self, timeout_magnitude):
        self.timeout_magnitude = timeout_magnitude
        return self

    def set_features(self, features: List[DataFeature]):
        self.features = features
        return self

    def to_string(self):
        return "Service {}: processing_magnitude = {}, error_processing_magnitude = {}, timeout_magnitude {}, error_rate = {}, memory(bytes) {}, features: {}".format(
            self.name,
            self.processing_magnitude, 
            self.error_processing_magnitude,
            self.timeout_magnitude,
            self.error_rate,
            self.max_memory_byte,
            len(self.features))
    
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

class DataFeatureNameRepo:
    """ These could human readable and are re-used across classes but not necessarily in a consistent manner. Ex: persistence1, ... """
    def __init__(self):
        self.counter = 0
        self.names = set([])
    
    def add_name(self, name: str):
        self.names.add(name)
        return name

    def add_next_name(self):
        self.counter = self.counter + 1
        return self.add_name("Feature{}".format(self.counter))

    def add_names_auto(self, count: int):
        for i in range(count):
            self.add_next_name()
        return self

    def __len__(self):
        return len(self.names)

    def __str__(self):
        return "DataFeatureNameRepo: size {}".format(len(self))

    def has(self, name: str)->bool:
        return name in self.names

class DataFeatureRepo:
    """  Store a feature """
    def __init__(self):
        self.features = {}
    
    def add_datafeature(self, datafeature: DataFeature):
        self.features[datafeature.name] = datafeature
        return self

    def remove_datafeature(self, datafeature: DataFeature):
        if datafeature.name in self.features:
            del self.features[datafeature.name]
        return self

    def __len__(self):
        return len(self.features)

    def __str__(self):
        return "DataFeatureRepo: size {}".format(len(self))

    def has(self, name: str)->bool:
        return name in self.features

    def choice(self)->DataFeature:
        return self.features[choice(list(self.features.keys()))]

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
        return self.add_name("Service{}".format(self.counter))

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

    def get_names(self)->List[str]:
        return list(self.dataservices.keys())

    def get_by_name(self, name: str):
        return self.dataservices[name]

class RandRange:
    def __init__(self, start: int, stop: int):
        self.start = 0
        self.stop = 10

    @classmethod
    def from_obj(cls, content):
        return cls(content["start"], content["stop"])

    def random(self):
        return randint(self.start, self.stop)

    def __str__(self):
        return "RandRange: [{}, {}]".format(self.start, self.stop)

class DataSystemConfig:
    def __init__(self):
        self.datatype_count_range = RandRange(1, 50)
        self.class_count_range = RandRange(1, 50)
        self.service_count_range = RandRange(1, 50)
        self.feature_count_range = RandRange(1, 50)
        self.reusable_property_count_range = RandRange(100, 500)
        self.property_count_range = RandRange(1, 50)
        self.service_feature_count_range = RandRange(1, 5)
        self.max_items_range = RandRange(1, 1000)
        self.max_memory_byte_range = RandRange(1000000, 100000000)
        self.proc_micro_sec_range = RandRange(1, 20)
        self.error_rate_range = RandRange(2, 8)
        self.timeout_magnitude_range = RandRange(20, 27)
        self.category_names = []

    def __str__(self):
        return ";".join([
            "datatype_count_range=",
            str(self.datatype_count_range),
            "class_count_range=",
            str(self.class_count_range),
            "service_count_range=",
            str(self.service_count_range),
            "feature_count_range=",
            str(self.feature_count_range),
            "reusable_property_count_range=",
            str(self.reusable_property_count_range),
            "property_count_range=",
            str(self.property_count_range),
            "service_feature_count_range=",
            str(self.service_feature_count_range),
            "max_items_range=",
            str(self.max_items_range),
            "max_memory_byte_range=",
            str(self.max_memory_byte_range),
            "proc_micro_sec_range=",
            str(self.proc_micro_sec_range),
            "error_rate_range=",
            str(self.error_rate_range),
            "timeout_magnitude_range=",
            str(self.timeout_magnitude_range),
             "category_names",
           str(self.category_names)
        ])

    @classmethod
    def from_obj(cls, content):
        config = cls()
        config.set_datatype_count_range(RandRange.from_obj(content["datatype-count-range"]))
        config.set_class_count_range(RandRange.from_obj(content["class-count-range"]))
        config.set_service_count_range(RandRange.from_obj(content["service-count-range"]))
        config.set_feature_count_range(RandRange.from_obj(content["feature-count-range"]))
        config.set_reusable_property_count_range(RandRange.from_obj(content["reusable-property-count-range"]))
        config.set_property_count_range(RandRange.from_obj(content["property-count-range"]))
        config.set_service_feature_count_range(RandRange.from_obj(content["service-feature-count-range"]))
        config.set_max_items_range(RandRange.from_obj(content["max-items-range"]))
        config.set_max_memory_byte_range(RandRange.from_obj(content["max-memory-byte-range"]))
        config.set_proc_micro_sec_range(RandRange.from_obj(content["proc-micro-sec-range"]))
        config.set_error_rate_range(RandRange.from_obj(content["error-rate-range"]))
        config.set_timeout_magnitude_range(RandRange.from_obj(content["timeout-magnitude-range"]))
        config.set_category_names(content["category-names"])

    def set_datatype_count_range(self, datatype_count_range: RandRange):
        self.datatype_count_range = datatype_count_range
        return self

    def set_class_count_range(self, class_count_range: RandRange):
        self.class_count_range = class_count_range
        return self

    def set_feature_count_range(self, feature_count_range: RandRange):
        self.feature_count_range = feature_count_range
        return self

    def set_service_count_range(self, service_count_range: RandRange):
        self.service_count_range = service_count_range
        return self
    
    def set_reusable_property_count_range(self, reusable_property_count_range: RandRange):
        self.reusable_property_count_range = reusable_property_count_range
        return self

    def set_property_count_range(self, property_count_range: RandRange):
        self.property_count_range = property_count_range
        return self

    def set_service_feature_count_range(self, service_feature_count_range: RandRange):
        self.service_feature_count_range = service_feature_count_range
        return self

    def set_max_items_range(self, max_items_range: RandRange):
        self.max_items_range = max_items_range
        return self

    def set_max_memory_byte_range(self, max_memory_byte_range: RandRange):
        self.max_memory_byte_range = max_memory_byte_range
        return self

    def set_proc_micro_sec_range(self, proc_micro_sec_range: RandRange):
        self.proc_micro_sec_range = proc_micro_sec_range
        return self

    def set_error_rate_range(self, error_rate_range: RandRange):
        self.error_rate_range = error_rate_range
        return self

    def set_timeout_magnitude_range(self, timeout_magnitude_range: RandRange):
        self.timeout_magnitude_range = timeout_magnitude_range
        return self

    def set_category_names(self, category_names: List[str]):
        self.category_names = category_names
        return self

class DataSystem:
    def __init__(self, config: DataSystemConfig):
        self.config = config
        self.data_property_type_repo = DataPropertyTypeRepo()
        self.data_property_name_repo = DataPropertyNameRepo()
        self.data_class_name_repo = DataClassNameRepo()
        self.data_class_repo = DataClassRepo()
        self.data_feature_name_repo = DataFeatureNameRepo()
        self.data_feature_repo = DataFeatureRepo()
        self.data_service_name_repo = DataServiceNameRepo()
        self.data_service_repo = DataServiceRepo()
        self.root_service = None
        
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

    def add_datafeature_auto(self)->DataFeature:
        dataFeature = DataFeature()
        dataFeature.set_name(self.data_feature_name_repo.add_next_name())
        self.data_feature_repo.add_datafeature(dataFeature)
        return dataFeature

    def add_datatypes_auto(self):
        self.data_property_type_repo.add_types_as_str("Bool Int Float")
        self.data_property_type_repo.add_types(["Type{}".format(i) for i in range(self.config.datatype_count_range.random())])

    def add_property_names_auto(self):
        self.data_property_name_repo.add_names_auto(self.config.reusable_property_count_range.random())

    def add_basic_datafeature_auto(self):
        for _ in range(self.config.feature_count_range.random()):
            dataFeature = self.add_datafeature_auto()
            dataFeature.set_name(choice(self.config.category_names))

    def add_basic_dataservice_auto(self):
        for _ in range(self.config.service_count_range.random()):
            dataService = self.add_dataservice_auto()
            dataService.set_processing_magnitude(self.config.proc_micro_sec_range.random())
            dataService.set_error_processing_magnitude(self.config.proc_micro_sec_range.random())
            dataService.set_error_rate(Fraction(1, 10**self.config.error_rate_range.random()))
            dataService.set_max_memory_byte(self.config.max_memory_byte_range.random())
            dataService.set_timeout_magnitude(self.config.timeout_magnitude_range.random())
            dataService.set_features([self.data_feature_repo.choice() for _ in range(self.config.service_feature_count_range.random())])
    
    def add_root_service_auto(self):
        self.root_service = self.data_service_repo.get_by_name(choice(self.data_service_repo.get_names()))

    def add_basic_dataclass_auto(self):
        for _ in range(self.config.class_count_range.random()):
            dataClass = self.add_dataclass_auto()
            propertyNames = self.data_property_name_repo.sample(self.config.property_count_range.random())
            for pname in propertyNames:
                prop = DataProperty()
                prop.set_name(pname)
                prop.set_max_items(self.config.max_items_range.random())
                prop.set_min_items(randint(0, prop.max_items))
                prop.set_datatype(self.data_property_type_repo.random_simple_type())
                dataClass.add(prop)

    def prepare(self):
        self.add_datatypes_auto()
        self.add_property_names_auto()
        self.add_basic_datafeature_auto()
        self.add_basic_dataservice_auto()
        self.add_root_service_auto()
        self.add_basic_dataclass_auto()


    def __str__(self):
        return "DataSystem: {}, {}, {}, {}".format(self.data_property_type_repo, self.data_class_repo, self.data_service_repo, self.root_service)
