def get_differing_keys(dict1, dict2):
        mismatched_attrs = {key: dict1[key]
                    for key in dict1
                    if dict1.get(key) != dict2.get(key)}

        return mismatched_attrs

def get_differing_kvp(source_dict, mismatched_attrs):
        return {key: source_dict[key] for key in source_dict if key in mismatched_attrs}

def dict_diff(source_dict,comparison_dict):
    mismatched_attrs = get_differing_keys(source_dict, comparison_dict)
    return get_differing_kvp(source_dict, mismatched_attrs)
