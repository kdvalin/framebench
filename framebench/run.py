from .models import config
from .test import CameraTest

import logging
import csv
import time


def run(device: str, test_time: int = 30, resolution="640x480", framerate=30, input_format="mjpeg", output="-"):
    """Run benchmark with the provided device

    :param device: The video device which will be used.
    :param test_time: The time (in seconds) to run the benchmark for.
    :param resolution: The desired resolution of the camera
    :param framerate: The desired framerate of the camera
    :param format: The format to be used (must be 4 characters, use `list` to validate what is supported on a camera)
    """
    test = CameraTest(device, test_time, input_format, resolution, framerate)
    test.run()
    results = test.get_results()
    test.cleanup()