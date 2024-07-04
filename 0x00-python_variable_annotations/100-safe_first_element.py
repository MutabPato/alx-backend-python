#!/usr/bin/env python3
"""Python - Variable Annotations"""
from typing import List, Any, Union, Tuple, Callable, Sequence, Iterable


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """Function annotation"""
    if lst:
        return lst[0]
    else:
        return None
