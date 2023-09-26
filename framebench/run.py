from .models import config
from .test import CameraTest

import logging
import csv
import time

from multiprocessing.shared_memory import SharedMemory
from multiprocessing import Process, Queue

import yaml
import pandas as pd

READY_MEM_NAME="framebench_all_ready"
READY_MEM_SIZE=1

def _run_test(device: str, test_time: int = 30, resolution="640x480", framerate=30, format="MJPG"):
    test = CameraTest(device)
    test.run()
    

def run(device: str, test_time: int = 30, resolution="640x480", framerate=30, format="MJPG", output="timings.csv"):
    """Run benchmark with the provided device

    :param device: The video device which will be used.
    :param test_time: The time (in seconds) to run the benchmark for.
    :param resolution: The desired resolution of the camera
    :param framerate: The desired framerate of the camera
    :param format: The format to be used (must be 4 characters, use `list` to validate what is supported on a camera)
    """
    _run_test(device)    