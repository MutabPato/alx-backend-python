#!/usr/bin/env python3
"""Python - Variable Annotations"""
from typing import List, Any, Union, Tuple
import math


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """a type-annotated function to_kv that takes a string k and
    an int OR float v as arguments and returns a tuple"""
    return (k, v * v)
