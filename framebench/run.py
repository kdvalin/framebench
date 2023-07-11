from .models import config
from .test import CamTest

import logging
import csv

import yaml
import pandas as pd 


def run(device: str, test_time: int = 30, resolution="640x480", framerate=30, format="MJPG", output="timings.csv"):
    """Run benchmark with the provided device

    :param device: The video device which will be used.
    :param test_time: The time (in seconds) to run the benchmark for.
    :param resolution: The desired resolution of the camera
    :param framerate: The desired framerate of the camera
    :param format: The format to be used (must be 4 characters, use `list` to validate what is supported on a camera)
    """
    test = CamTest(device, resolution, framerate, format, test_time)
    test.start()
    test.join()
    
    pd.DataFrame(test.get_result()).to_csv(output, index=False, header=False)

def run_multiple(config_path: str, output: str = "timings.csv"):
    cols = []

    with open(config_path, 'r') as config_file:
        config_obj: config.Config = config.Config.parse_obj(yaml.safe_load(config_file))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(config_obj.cams)) as exeutor:
        thread_pool = []
        for cam in config_obj.cams:
            args = [
                cam.path,
                config_obj.test_time,
                cam.resolution,
                cam.framerate,
                cam.stream_format
            ]
            thread_pool.append((cam.path, exeutor.submit(run, *args)))

        for thread in thread_pool:
            cols.append([thread[0], *thread[1].result()])
    pd.DataFrame(cols).transpose().to_csv(output)
    