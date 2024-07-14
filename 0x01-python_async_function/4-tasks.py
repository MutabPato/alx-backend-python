#!/usr/bin/env python3
"""Python - Async"""


import asyncio
from typing import List
import heapq


task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """spawn wait_random n times with the specified max_delay"""
    tasks = [task_wait_random(max_delay) for _ in range(n)]
    delays = await asyncio.gather(*tasks)
    sorted_delays = list(heapq.nsmallest(len(delays), delays))
    return sorted_delays
