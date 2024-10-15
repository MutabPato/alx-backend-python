#!/usr/bin/env python3
"""Python - Async"""


import asyncio
import random


async def wait_random(max_delay=10):
    """The basics of async"""
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
