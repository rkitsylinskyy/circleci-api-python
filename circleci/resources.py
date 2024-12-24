""" This file contains the CircleCIResource class and the CircleCIPropertyHolder class """


class CircleCIPropertyHolder:
    """
    A class to hold the properties of a CircleCI resource
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def dict_to_circleci_resource(data, is_first_iteration=True):
    """
    This function converts a dictionary to a CircleCIPropertyHolder object

    Args:
        data (dict): The dictionary to convert
        is_first_iteration (bool): A flag to determine if this is the first iteration

    Returns:
        CircleCIPropertyHolder: The converted CircleCIProperty
    """
    if isinstance(data, dict):
        property_holder_kwargs = {k: dict_to_circleci_resource(
            v,
            is_first_iteration=False) for k, v
            in data.items()}
        if is_first_iteration:
            del data['metadata']
            if data:
                property_holder_kwargs['raw_data'] = data
        return CircleCIPropertyHolder(**property_holder_kwargs)
    if isinstance(data, list):
        return [dict_to_circleci_resource(
            item,
            is_first_iteration=False) for item in data]
    return data
