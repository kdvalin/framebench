from .models import config
from .test import CameraTest

import pandas as pd

import logging
import time
import sys


def run(device: str, test_time: int = 30, resolution="640x480", framerate=30, input_format="mjpeg", output="-"):
    """Run benchmark with the provided device

    :param device: The video device which will be used.
    :param test_time: The time (in seconds) to run the benchmark for.
    :param resolution: The desired resolution of the camera
    :param framerate: The desired framerate of the camera
    :param format: The format to be used (use `list` to validate what is supported on a camera, MJPG is mjpeg)
    """
    test = CameraTest(device, test_time, input_format, resolution, framerate)
    test.run()
    results = test.get_results()
    test.cleanup()

    file = sys.stdout if output == '-' else open(output, 'w')

    df = pd.DataFrame(data=results)
    df.to_csv(file, index=False)
    file.close()
