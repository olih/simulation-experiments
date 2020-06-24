from fractions import Fraction
from typing import List, Tuple, Set
from enum import Enum, auto
from random import sample, choice, randint, uniform
from math import log

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

    def get_service_name(self):
        if self.is_ref():
            return self.datatype.split(":")[0]
        else:
            return None
    
    def get_dataname(self):
        if self.is_ref():
            return self.datatype.split(":")[1]
        else:
            return None

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

    def is_ref(self):
        return self.datatype.is_ref()

    def get_weight(self)->int:
        return 1 + self.min_items + (self.max_items - self.min_items) // 2
    

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
        return "name = {}\n----\n".format(self.name) + "\n".join([str(p) for p in list(self.properties)])
    
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

    def get_ref_datatypes(self)->Set[DataPropertyType]:
        return set([p for p in self.properties if p.is_ref])

    def get_simple_datatypes(self)->Set[DataPropertyType]:
        return set([p for p in self.properties if not p.is_ref])

    def get_weight(self)->int:
        return sum([p.get_weight() for p in self.properties])

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

class DataRequirement:
    """A requirement that are needed for the service"""
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
        return "DataRequirement: {}, category: {}".format(self.name, self.category_name)
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

    def set_requirements(self, requirements: List[DataRequirement]):
        self.requirements = requirements
        return self

    def to_string(self):
        return "Service {}: processing_magnitude = {}, error_processing_magnitude = {}, timeout_magnitude {}, error_rate = {}, memory(bytes) {}, features: {}, requirements: {}".format(
            self.name,
            self.processing_magnitude, 
            self.error_processing_magnitude,
            self.timeout_magnitude,
            self.error_rate,
            self.max_memory_byte,
            len(self.features),
            len(self.requirements)
            )
    
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

    def random_type(self, isref: bool)->DataPropertyType:
        return self.random_ref_type() if isref else self.random_simple_type()

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

    def get_names(self)->List[str]:
        return list(self.names)

    def choice(self)->str:
        return choice(self.get_names())


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

class DataRequirementNameRepo:
    """ These could human readable and are re-used across classes but not necessarily in a consistent manner. Ex: persistence1, ... """
    def __init__(self):
        self.counter = 0
        self.names = set([])
    
    def add_name(self, name: str):
        self.names.add(name)
        return name

    def add_next_name(self):
        self.counter = self.counter + 1
        return self.add_name("Requirement{}".format(self.counter))

    def add_names_auto(self, count: int):
        for i in range(count):
            self.add_next_name()
        return self

    def __len__(self):
        return len(self.names)

    def __str__(self):
        return "DataRequirementNameRepo: size {}".format(len(self))

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

class DataRequirementRepo:
    """  Store a requirement """
    def __init__(self):
        self.requirements = {}
    
    def add_datarequirement(self, datarequirement: DataRequirement):
        self.requirements[datarequirement.name] = datarequirement
        return self

    def remove_datafeature(self, datarequirement: DataRequirement):
        if datarequirement.name in self.requirements:
            del self.requirements[datarequirement.name]
        return self

    def __len__(self):
        return len(self.requirements)

    def __str__(self):
        return "DataRequirementRepo: size {}".format(len(self))

    def has(self, name: str)->bool:
        return name in self.requirements

    def choice(self)->DataRequirement:
        return self.requirements[choice(list(self.requirements.keys()))]

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

    def get_dataclasses(self)->List[DataClass]:
        return list(self.dataclasses.values())

    def get_by_name(self, name: str):
        try:
            found = self.dataclasses[name]
            return found
        except:
            raise Exception("No dataclass {} found".format(name))

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

    def get_services(self)->List[DataService]:
        return list(self.dataservices.values())
    
    def get_by_name(self, name: str):
        try:
            found = self.dataservices[name]
            return found
        except:
            raise Exception("No service {} found".format(name))
        

    def choice(self)->DataService:
        return self.dataservices[choice(list(self.dataservices.keys()))]

class RandRange:
    def __init__(self, start: int, stop: int):
        self.start = start
        self.stop = stop

    @classmethod
    def from_obj(cls, content):
        return cls(int(content["start"]), int(content["stop"]))

    def random(self):
        return randint(self.start, self.stop)

    def __str__(self):
        return "RandRange: [{}, {}]".format(self.start, self.stop)

class RatioRange:
    def __init__(self, start: Fraction, stop: Fraction):
        self.start = start
        self.stop = stop

    @classmethod
    def from_obj(cls, content):
        return cls(Fraction(content["start"]), Fraction(content["stop"]))

    def random_float(self)->float:
        return uniform(float(self.start), float(self.stop))

    def random_int(self, scale: int)->int:
        return int(self.random_float()*scale)

    def should_activate(self)->bool:
        return uniform(0.0, 1.0) <= self.random_float()

    def __str__(self):
        return "RatioRange: [{}, {}]".format(self.start, self.stop)

class DataSystemConfig:
    def __init__(self):
        self.datasystem_count = 50
        self.simple_datatype_count_range = RandRange(1, 50)
        self.ref_datatype_ratio_range = RatioRange(Fraction(1, 20), Fraction(2, 20))
        self.class_count_range = RandRange(1, 50)
        self.service_count_range = RandRange(1, 50)
        self.feature_count_range = RandRange(1, 50)
        self.requirement_count_range = RandRange(1, 50)
        self.reusable_property_count_range = RandRange(100, 500)
        self.property_count_range = RandRange(1, 50)
        self.ref_property_ratio_range = RatioRange(Fraction(1, 20), Fraction(2, 20))
        self.service_feature_count_range = RandRange(1, 5)
        self.service_requirement_count_range = RandRange(1, 5)
        self.service_requirement_ratio_range = RatioRange(Fraction(1, 20), Fraction(2, 20))
        self.max_items_range = RandRange(1, 1000)
        self.max_memory_byte_range = RandRange(1000000, 100000000)
        self.proc_micro_sec_range = RandRange(1, 20)
        self.error_rate_range = RandRange(2, 8)
        self.timeout_magnitude_range = RandRange(20, 27)
        self.feature_category_names = []
        self.requirement_category_names = []

    def __str__(self):
        return ";".join([
            "datasystem_count=",
            str(self.datasystem_count),
            "simple_datatype_count_range=",
            str(self.simple_datatype_count_range),
            "ref_datatype_ratio_range=",
            str(self.ref_datatype_ratio_range),
            "class_count_range=",
            str(self.class_count_range),
            "service_count_range=",
            str(self.service_count_range),
            "feature_count_range=",
            str(self.feature_count_range),
            "requirement_count_range=",
            str(self.requirement_count_range),
            "reusable_property_count_range=",
            str(self.reusable_property_count_range),
            "property_count_range=",
            str(self.property_count_range),
            "ref_property_ratio_range=",
            str(self.ref_property_ratio_range),
            "service_feature_count_range=",
            str(self.service_feature_count_range),
            "service_requirement_count_range=",
            str(self.service_requirement_count_range),
            "service_requirement_ratio_range=",
            str(self.service_requirement_ratio_range),
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
            "feature_category_names",
            str(self.feature_category_names),
            "requirement_category_names",
            str(self.requirement_category_names)
       ])

    @classmethod
    def from_obj(cls, content):
        config = cls()
        config.set_datasystem_count(int(content["datasystem-count"]))
        config.set_simple_datatype_count_range(RandRange.from_obj(content["simple-datatype-count-range"]))
        config.set_ref_datatype_ratio_range(RatioRange.from_obj(content["ref-datatype-ratio-range"]))
        config.set_class_count_range(RandRange.from_obj(content["class-count-range"]))
        config.set_service_count_range(RandRange.from_obj(content["service-count-range"]))
        config.set_feature_count_range(RandRange.from_obj(content["feature-count-range"]))
        config.set_requirement_count_range(RandRange.from_obj(content["requirement-count-range"]))
        config.set_reusable_property_count_range(RandRange.from_obj(content["reusable-property-count-range"]))
        config.set_property_count_range(RandRange.from_obj(content["property-count-range"]))
        config.set_ref_property_ratio_range(RatioRange.from_obj(content["ref-property-ratio-range"]))
        config.set_service_feature_count_range(RandRange.from_obj(content["service-feature-count-range"]))
        config.set_service_requirement_count_range(RandRange.from_obj(content["service-requirement-count-range"]))
        config.set_service_requirement_ratio_range(RatioRange.from_obj(content["service-requirement-ratio-range"]))
        config.set_max_items_range(RandRange.from_obj(content["max-items-range"]))
        config.set_max_memory_byte_range(RandRange.from_obj(content["max-memory-byte-range"]))
        config.set_proc_micro_sec_range(RandRange.from_obj(content["proc-micro-sec-range"]))
        config.set_error_rate_range(RandRange.from_obj(content["error-rate-range"]))
        config.set_timeout_magnitude_range(RandRange.from_obj(content["timeout-magnitude-range"]))
        config.set_feature_category_names(content["feature-category-names"])
        config.set_requirement_category_names(content["requirement-category-names"])
        return config

    def set_datasystem_count(self, datasystem_count: int):
        self.datasystem_count = datasystem_count
        return self

    def set_simple_datatype_count_range(self, simple_datatype_count_range: RandRange):
        self.simple_datatype_count_range = simple_datatype_count_range
        return self

    def set_ref_datatype_ratio_range(self, ref_datatype_ratio_range: RatioRange):
        self.ref_datatype_ratio_range = ref_datatype_ratio_range
        return self

    def set_class_count_range(self, class_count_range: RandRange):
        self.class_count_range = class_count_range
        return self

    def set_feature_count_range(self, feature_count_range: RandRange):
        self.feature_count_range = feature_count_range
        return self

    def set_requirement_count_range(self, requirement_count_range: RandRange):
        self.requirement_count_range = requirement_count_range
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

    def set_ref_property_ratio_range(self, ref_property_ratio_range: RatioRange):
        self.ref_property_ratio_range = ref_property_ratio_range
        return self

    def set_service_feature_count_range(self, service_feature_count_range: RandRange):
        self.service_feature_count_range = service_feature_count_range
        return self

    def set_service_requirement_count_range(self, service_requirement_count_range: RandRange):
        self.service_requirement_count_range = service_requirement_count_range
        return self

    def set_service_requirement_ratio_range(self, service_requirement_ratio_range: RatioRange):
        self.service_requirement_ratio_range = service_requirement_ratio_range
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

    def set_feature_category_names(self, category_names: List[str]):
        self.feature_category_names = category_names
        return self

    def set_requirement_category_names(self, category_names: List[str]):
        self.requirement_category_names = category_names
        return self

class DataStat:
    def __init__(self):
        self.todo = ""

class ServiceAndClass:
    def __init__(self, service: DataService, dataclass: DataClass):
        self.service = service
        self.dataclass = dataclass

    def to_string(self):
        return "{} -> {}".format(self.service.name, self.dataclass.name)
    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()

class DataSystem:
    def __init__(self, config: DataSystemConfig):
        self.config = config
        self.data_property_type_repo = DataPropertyTypeRepo()
        self.data_property_name_repo = DataPropertyNameRepo()
        self.data_class_name_repo = DataClassNameRepo()
        self.data_class_repo = DataClassRepo()
        self.data_feature_name_repo = DataFeatureNameRepo()
        self.data_feature_repo = DataFeatureRepo()
        self.data_requirement_name_repo = DataRequirementNameRepo()
        self.data_requirement_repo = DataRequirementRepo()
        self.data_service_name_repo = DataServiceNameRepo()
        self.data_service_repo = DataServiceRepo()

    def get_services(self)->List[DataService]:
        return self.data_service_repo.get_services()

    def get_dataclasses(self)->List[DataClass]:
        return self.data_class_repo.get_dataclasses()

    def get_ref_types(self)->List[tuple]:
        return [ServiceAndClass(service=self.data_service_repo.get_by_name(rt.get_service_name()), dataclass = self.data_class_repo.get_by_name(rt.get_dataname())) for rt in self.data_property_type_repo.ref_types_as_list()]
 
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
    
    def add_datarequirement_auto(self)->DataRequirement:
        dataRequirement = DataRequirement()
        dataRequirement.set_name(self.data_requirement_name_repo.add_next_name())
        self.data_requirement_repo.add_datarequirement(dataRequirement)
        return dataRequirement

    def add_property_names_auto(self):
        self.data_property_name_repo.add_names_auto(self.config.reusable_property_count_range.random())

    def add_basic_datafeature_auto(self):
        for _ in range(self.config.feature_count_range.random()):
            dataFeature = self.add_datafeature_auto()
            dataFeature.set_category_name(choice(self.config.feature_category_names))

    def add_basic_datarequirement_auto(self):
        for _ in range(self.config.requirement_count_range.random()):
            dataRequirement = self.add_datarequirement_auto()
            dataRequirement.set_category_name(choice(self.config.requirement_category_names))

    def add_basic_dataservice_auto(self):
        for _ in range(self.config.service_count_range.random()):
            dataService = self.add_dataservice_auto()
            dataService.set_processing_magnitude(self.config.proc_micro_sec_range.random())
            dataService.set_error_processing_magnitude(self.config.proc_micro_sec_range.random())
            dataService.set_error_rate(Fraction(1, 10**self.config.error_rate_range.random()))
            dataService.set_max_memory_byte(self.config.max_memory_byte_range.random())
            dataService.set_timeout_magnitude(self.config.timeout_magnitude_range.random())
            dataService.set_features([self.data_feature_repo.choice() for _ in range(self.config.service_feature_count_range.random())])
            if self.config.service_requirement_ratio_range.should_activate():
                dataService.set_requirements([self.data_requirement_repo.choice() for _ in range(self.config.service_requirement_count_range.random())])
            else:
                dataService.set_requirements([])
    
    def add_dataclass_names_auto(self):
        for _ in range(self.config.class_count_range.random()):
            self.data_class_name_repo.add_next_name()

    def add_datatypes_auto(self):
        simple_count = self.config.simple_datatype_count_range.random()
        simple_types = ["Type{}".format(i) for i in range(simple_count)]
        min_ref_types = ["{}:{}".format(self.data_service_repo.choice().name, dataclassname) for dataclassname in self.data_class_name_repo.get_names()]
        ref_count = self.config.ref_datatype_ratio_range.random_int(simple_count) - len(min_ref_types)
        ref_types = ["{}:{}".format(self.data_service_repo.choice().name, self.data_class_name_repo.choice()) for _ in range(ref_count)]
        created_types =  simple_types + min_ref_types + ref_types
        self.data_property_type_repo.add_types(created_types)
        self.data_property_type_repo.add_types_as_str("Bool Char Int Float")

    def add_basic_dataclass_auto(self):
        for name in self.data_class_name_repo.get_names():
            dataClass = DataClass()
            dataClass.set_name(name)
            self.data_class_repo.add_dataclass(dataClass)
            propertyNames = self.data_property_name_repo.sample(self.config.property_count_range.random())
            for pname in propertyNames:
                prop = DataProperty()
                prop.set_name(pname)
                prop.set_max_items(self.config.max_items_range.random())
                prop.set_min_items(randint(0, prop.max_items))
                prop.set_datatype(self.data_property_type_repo.random_type(isref=self.config.ref_property_ratio_range.should_activate()))
                dataClass.add(prop)

    def prepare(self):
        self.add_property_names_auto()
        self.add_basic_datafeature_auto()
        self.add_basic_datarequirement_auto()
        self.add_basic_dataservice_auto()
        self.add_dataclass_names_auto()
        self.add_datatypes_auto()
        self.add_basic_dataclass_auto()


    def __str__(self):
        return "DataSystem: {}, {}, {}, {}, {}, {}".format(
            self.data_property_type_repo,
            self.data_property_name_repo,
            self.data_class_repo,
            self.data_service_repo,
            self.data_feature_repo,
            self.data_requirement_repo,
            )

    
    def get_stats_by_refdatatype(self, refdatatype: str, limit = 5):
        return 0

class ServiceCost:
    def __init__(self):
        self.feature_coeff = Fraction(1, 1)
        self.error_rate_coeff = Fraction(1, 1)
        self.max_memory_byte_coeff = Fraction(1, 1)

    def set_feature_coeff(self, value: Fraction):
        self.feature_coeff = value
        return self

    def set_error_rate_coeff(self, value: Fraction):
        self.error_rate_coeff = value
        return self

    def set_max_memory_byte_coeff(self, value: Fraction):
        self.max_memory_byte_coeff = value
        return self

    @classmethod
    def from_obj(cls, content):
        calc = cls()
        calc.set_feature_coeff(Fraction(content["feature-coeff"]))
        calc.set_error_rate_coeff(Fraction(content["error-rate-coeff"]))
        calc.set_max_memory_byte_coeff(Fraction(content["max-memory-byte-coeff"]))
        return calc
    
    def __str__(self):
        return "ServiceCost: feature: {}, error rate {}, memory {}".format(self.feature_coeff, self.error_rate_coeff, self.max_memory_byte_coeff)

    def get_cost(self, service: DataService)->Fraction:
        higher_is_better = self.feature_coeff*len(service.features) + self.max_memory_byte_coeff*log(service.max_memory_byte, 5) - self.error_rate_coeff*log(service.error_rate, 10)
        return  higher_is_better