#!/usr/bin/env python3.8
# https://blog.devgenius.io/why-is-multi-threaded-python-so-slow-f032757f72dc
"""
Test 1: The baseline test without threads or using
any packages.
"""
import time


def vThreadFunction():
    """Function to do CPU-bound work.
    Args:
    Returns:
    """

    iResult = 0
    for iCnt in range(50000000):
        iResult += iCnt


def vMain():
    fTimePrefCountStart = time.perf_counter()

    # Call the function eight times
    for _ in range(8):
        vThreadFunction()

    fTimePrefCountEnd = time.perf_counter()
    print(f"Delta time {fTimePrefCountEnd - fTimePrefCountStart} [s]")


if __name__ == "__main__":
    vMain()