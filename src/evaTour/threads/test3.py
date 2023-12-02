#!/usr/bin/env python3.8
"""
Test 3: Making use of the ThreadPoolExecutor
from the concurrent package.
"""
import time
from concurrent.futures import ThreadPoolExecutor, wait


def iThreadFunction():
    """Function to do CPU-bound work.
    Args:
    Returns:
    """
    iResult = 0

    for i in range(50000000):
        iResult += i


def vMain():
    # Create an executor with a maximum of eight workers
    objExecutor = ThreadPoolExecutor(max_workers=8)

    lstFutures = []

    fTimePrefCountStart = time.perf_counter()

    # Submit eight tasks to the executor
    for _ in range(8):
        lstFutures.append(objExecutor.submit(iThreadFunction))

    # Wait for all threads to complete
    wait(lstFutures)

    fTimePrefCountEnd = time.perf_counter()
    print(f"Delta time {fTimePrefCountEnd - fTimePrefCountStart} [s]")

    objExecutor.shutdown(wait=False)


if __name__ == "__main__":
    vMain()