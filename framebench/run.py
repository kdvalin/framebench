from .models import config
from .proc_manager import ProcessManager
from .test import CameraTest, process_main
from .consts import READY_MEM_NAME, READY_MEM_SIZE

import pandas as pd

import yaml
import logging
import sys

from multiprocessing import Process, Queue

def write_to_file(data: pd.DataFrame, dest: str):
    file = sys.stdout if dest == '-' else open(dest, 'r')
    data.to_csv(file, index=False, header=False)
    file.close()

def run_multiple(config_file: str, output: str = "-"):
    file: config.Config = config.Config.parse_obj(
        yaml.safe_load(
            open(config_file, "r")
        )
    )
    cols = []
    proc_man = ProcessManager()
    for cam in file.cams:
        proc_man.add_process(
            target=process_main,
            args=(
                proc_man.results_queue,
                cam.path,
                file.test_time,
                cam.stream_format,
                cam.resolution,
                cam.framerate
            )
        )
    
    proc_man.start_processes()
    proc_man.wait_until_ready()
    proc_man.trigger_ready()
    
    for result in proc_man.results():
        cols.append(result)

    write_to_file(pd.DataFrame(cols).transpose(), output)


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

    write_to_file(pd.DataFrame(data=results), output)
