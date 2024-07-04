#!/usr/bin/env python3
"""Python - Variable Annotations"""
from typing import List, Any, Union, Tuple, Callable
import math


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """a type-annotated function make_multiplier that takes a float
    multiplier as argument and returns a function that multiplies a
    float by multiplier"""
    def multiply(multiplier):
        return multiplier * multiplier
    return (multiply)
