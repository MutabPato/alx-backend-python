#!/usr/bin/env python3
"""Python - Variable Annotations"""
from typing import List, Any, Union, Tuple, Callable, Sequence, Iterable


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """Function annotation"""
    return [(i, len(i)) for i in lst]
