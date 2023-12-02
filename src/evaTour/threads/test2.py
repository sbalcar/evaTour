#!/usr/bin/env python3.8
"""
Test 2: Making use of the threading module to spawn
eight threads.
"""
import threading
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
    lstThreads = []

    fTimePrefCountStart = time.perf_counter()

    # Create eight threads
    for _ in range(8):
        objThread = threading.Thread(target=vThreadFunction)
        objThread.daemon = False
        lstThreads.append(objThread)

    for objThread in lstThreads:
        objThread.start()

    for objThread in lstThreads:
        objThread.join()

    fTimePrefCountEnd = time.perf_counter()
    print(f"Delta time {fTimePrefCountEnd - fTimePrefCountStart} [s]")

    return


if __name__ == "__main__":
    vMain()