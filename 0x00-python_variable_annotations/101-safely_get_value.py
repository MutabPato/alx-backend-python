#!/usr/bin/env python3
"""Python - Variable Annotations"""
from typing import List, Any, Union, Tuple, TypeVar, Mapping


T = TypeVar('T')


def safely_get_value(
        dct: Mapping, key: Any, default: Union[
            T, None] = None) -> Union[Any, T]:
    """Function annotation"""
    if key in dct:
        return dct[key]
    else:
        return default
