from typing import List, Tuple, Dict, Set
from random import sample, choice, randint, uniform
from math import log, floor, ceil
from fractions import Fraction
import csv


class NumberRange:
    def random_int(self)->int:
        pass
    def random_float(self)->float:
        pass

class IntRange(NumberRange):
    def __init__(self, start: int, stop: int):
        self.start = start
        self.stop = stop

    @classmethod
    def from_obj(cls, content):
        return cls(int(content["start"]), int(content["stop"]))

    def random_int(self):
        diff_range = self.stop - self.start
        if diff_range <=100:
            return randint(self.start, self.stop)
        else:
            divisions = int(ceil(log(diff_range,10)))
            expof10 = randint(1, divisions)
            mindec = min(10 ** (expof10-1), self.start)
            maxdec = max(10 ** expof10, self.stop)
            return randint(mindec, maxdec)

    def random_float(self):
        return float(self.random_int())

    def __str__(self):
        return "[{}, {}]".format(self.start, self.stop)

class FractionRange(NumberRange):
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

    def __str__(self):
        return "[{}, {}]".format(self.start, self.stop)


header_review_time_second="review_time_s"
header_available_time_second="available_time_s"
header_available_time_hour="available_time_h"
header_success_ratio = "success"
header_reviewed_asset="reviewed_assets"
header_accepted_assets="accepted_assets"

class SimulationPoint:
    def __init__(self):
        self.review_time_second = 10
        self.available_time_second = 60
        self.success_ratio = float(0.01)
    
    def set_review_time_second(self, review_time_second: int):
        self.review_time_second = review_time_second
        return self

    def set_available_time_second(self, available_time_second: int):
        self.available_time_second = available_time_second
        return self

    def set_success_ratio(self, success_ratio: float):
        self.success_ratio = success_ratio
        return self

    def to_obj(self):
        return {
            f"{header_review_time_second}": self.review_time_second,
            f"{header_available_time_second}": self.available_time_second,
            f"{header_available_time_hour}": self.available_time_second // 3600,
            f"{header_success_ratio}": float(self.success_ratio),
            f"{header_reviewed_asset}": self.available_time_second // self.review_time_second,
            f"{header_accepted_assets}": int((self.available_time_second // self.review_time_second)*self.success_ratio)
        }
    def __str__(self):
        return str(self.to_obj())

class SimulationParams:
    def __init__(self):
        self.count = 10
        self.review_time_second: IntRange
        self.available_time_second: IntRange
        self.success_ratio: FractionRange

    def set_count(self, count: int):
        self.count = count
        return self

    def set_review_time_second(self, review_time_second: IntRange):
        self.review_time_second = review_time_second
        return self

    def set_available_time_second(self, available_time_second: IntRange):
        self.available_time_second = available_time_second
        return self

    def set_success_ratio(self, success_ratio: FractionRange):
        self.success_ratio = success_ratio
        return self

    def random_simulation_point(self)->SimulationPoint:
        point = SimulationPoint().set_review_time_second(self.review_time_second.random_int())
        point.set_available_time_second(self.available_time_second.random_int())
        point.set_success_ratio(self.success_ratio.random_float())
        return point

class Simulation:
    def __init__(self, config: SimulationParams):
        self.config = config

    def simulate(self)->List[SimulationPoint]:
        points = [SimulationPoint().set_available_time_second(self.config.available_time_second.random_int()) for _ in range(self.config.count)]
        return points

header_fieldnames: List[str] = [header_review_time_second, header_available_time_second, header_available_time_hour, header_success_ratio, header_reviewed_asset, header_accepted_assets]

def save_to_csv(filename, points: List[SimulationPoint]):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header_fieldnames)

        writer.writeheader()
        for p in points:
            writer.writerow(p.to_obj())
