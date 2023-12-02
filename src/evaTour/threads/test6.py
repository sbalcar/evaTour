#!/usr/bin/env python3.8
"""
Test 6: Combining ProcessPoolExecutor with
the asyncio package.
"""
import time
from concurrent.futures import ProcessPoolExecutor
import asyncio


def vProcessFunction():
    """Function to do CPU-bound work.
    Args:
    Returns:
    """
    iResult = 0
    for iCnt in range(50000000):
        iResult += iCnt


async def vMain():
    loop = asyncio.get_running_loop()

    lstFutures = []

    # Create an executor with a maximum of eight workers
    objExecutor = ProcessPoolExecutor(max_workers=8)

    fTimePrefCountStart = time.perf_counter()

    # Create eight processes using the executor
    for _ in range(8):
        lstFutures.append(loop.run_in_executor(objExecutor, vProcessFunction))

    # Wait for all processes to complete
    await asyncio.wait(lstFutures)

    fTimePrefCountEnd = time.perf_counter()
    print(f"Delta time {fTimePrefCountEnd - fTimePrefCountStart} [s]")


if __name__ == "__main__":
    # Python 3.7+
    asyncio.run(vMain())