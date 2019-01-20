from copy import deepcopy


def create_object_property_generator(obj, substitutions):
    obj_dict = deepcopy(obj.__dict__)
    obj_dict.update(substitutions)
    for key, value in obj_dict.items():
        yield key, value
