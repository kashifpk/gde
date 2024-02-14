"""Misc. functions to work with dictionaries and collections."""

from collections.abc import Mapping


def all_in(keys, collection):
    """Check if all given keys are present in the given collection/dict."""
    for key in keys:
        if key not in collection:
            return False

    return True


def any_in(keys, collection):
    """Check any of the given keys is present in the given collection/dict."""
    for key in keys:
        if key in collection:
            return True

    return False


def none_in(keys, collection):
    """Check that collection contains none of the given keys."""
    for key in keys:
        if key in collection:
            return False

    return True


def d_key_path_exists(keys, collection):
    """
    Check that the keys given exist recursively.

    First key is expected to be at parent level, second key in the child dict
    of parent and so on. For embedded lists index values like 0, 1, 2 can be
    used as keys.

    Returns a 2-item tuple, where first boolean value indicates if path exists
    or not and second value contains the value present at path or None if
    path does not exist.
    """
    new_c = collection
    for k in keys:
        if isinstance(new_c, Mapping):
            if k not in new_c:
                return (False, None)
        elif isinstance(new_c, (list, tuple)):
            if len(new_c) <= k:
                return (False, None)
        elif new_c is None:
            return (False, None)

        new_c = new_c[k]

    return (True, new_c)


def l_set_val(l_in, v):
    """
    Set a value for a list only if value is not already present.

    If l_in is None then a new list is created.
    """
    if l_in is None:
        l_in = []

    if v not in l_in:
        l_in.append(v)

    return l_in


def dict_set_if_exists(dd, d_key, sd, s_keys):
    """
    Set an item in dictionary dd with key set as d_key if s_keys exist in sd.
    """
    exists, val = d_key_path_exists(s_keys, sd)
    if exists:
        dd[d_key] = val


def dict_set_if_none_or_missing(d_in: dict, keys: list, value: any) -> bool:
    """
    Set value in dict at specified key-depth (nesting level) only if either the key heirarchy doesn't
    exist or it's value is None.
    """
    current = d_in
    keys_size = len(keys)

    for idx, k in enumerate(keys):
        if k not in current:
            if idx == (keys_size - 1):
                current[k] = None
            else:
                current[k] = {}

        if idx != (keys_size - 1):
            current = current[k]

    if current[k] is not None:
        return False

    current[k] = value

    return True


def value_lookup(keys, obj, call_callable=True):
    """
    Check that the keys given exist recursively in object,

    :param keys: List of keys to recursively lookup. First key is expected to
        be at parent level, second key in the child dict of parent and so on.
        For embedded lists index values like 0, 1, 2 can be used as keys.
        Can also be a string in which case it is expected to be a dot notation
        starting from . (for example .details.certificates.0.certificate.0.not_after)
    :param obj: The object to look into (can be object, list or dict).
    :param call_callabe: If current value is a callable function (without any
        args then call it.)

    Returns a 2-item tuple, where first boolean value indicates if path exists
    or not and second value contains the value present at path or None if
    path does not exist.
    """
    new_obj = obj
    if isinstance(keys, str) and keys.startswith('.'):
        keys = keys.lstrip(".").split(".")

    for k in keys:
        if isinstance(new_obj, Mapping):
            if k not in new_obj:
                return (False, None)

            new_obj = new_obj[k]

        elif isinstance(new_obj, (list, tuple)):
            # see if key can be converted to int.
            k = int(k)
            if len(new_obj) <= k:
                return (False, None)

            new_obj = new_obj[k]

        else:
            if not hasattr(new_obj, k):
                return (False, None)

            if callable(getattr(new_obj, k)) and call_callable:
                new_obj = getattr(new_obj, k)()
            else:
                new_obj = getattr(new_obj, k)

    return (True, new_obj)


def value_replace(keys, obj, new_val):
    """
    Check that the keys given exist recursively in object and replace the last
    key, index or property with given new_val.

    :param keys: List of keys to recursively lookup. First key is expected to
        be at parent level, second key in the child dict of parent and so on.
        For embedded lists index values like 0, 1, 2 can be used as keys.
    :param obj: The object to look into (can be object, list or dict).
    :param new_Val: New value to be set as value of obj's keys[-1] value.

    Returns True or False indicating if value was found and replaced.
    """
    new_obj = obj

    last_idx = len(keys) - 1
    for idx, k in enumerate(keys):
        if isinstance(new_obj, Mapping):
            if k not in new_obj:
                return False

            if idx == last_idx:
                new_obj[k] = new_val
                return True
            else:
                new_obj = new_obj[k]

        elif isinstance(new_obj, list):  # replace won't work on tuples
            if len(new_obj) <= k:
                return False

            if idx == last_idx:
                new_obj.insert(k, new_val)
                del new_obj[k + 1]
                return True
            else:
                new_obj = new_obj[k]

        else:
            if not hasattr(new_obj, k):
                return False

            if idx == last_idx:
                setattr(new_obj, k, new_val)
                return True
            else:
                new_obj = getattr(new_obj, k)

    return False
