from copy import deepcopy
from abc import ABC, abstractmethod


class CustomJSONSerialization(ABC):
    @abstractmethod
    def to_json(self):
        pass


def obj_to_json(obj, substitutions):
    obj_dict = deepcopy(obj.__dict__)
    obj_dict.update(substitutions)
    return obj_dict
