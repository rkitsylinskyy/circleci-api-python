class CircleCIPropertyHolder:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def dict_to_circleci_resource(data, is_first_iteration=True):
    if isinstance(data, dict):
        property_holder_kwargs = {k: dict_to_circleci_resource(v, is_first_iteration=False) for k, v
                                  in data.items()}
        if is_first_iteration:
            del data['metadata']
            if data:
                property_holder_kwargs['raw_data'] = data
        return CircleCIPropertyHolder(**property_holder_kwargs)
    elif isinstance(data, list):
        return [dict_to_circleci_resource(item, is_first_iteration=False) for item in data]
    else:
        return data
