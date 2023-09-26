from .models import config
from .test import CameraTest, process_main
from .consts import READY_MEM_NAME, READY_MEM_SIZE

import pandas as pd

import yaml
import logging
import sys

from multiprocessing import Process, Queue
from multiprocessing.shared_memory import SharedMemory


def run_multiple(config_file: str, output: str = "-"):
    file: config.Config = config.Config.parse_obj(
        yaml.safe_load(
            open(config_file, "r")
        )
    )
    cols = []
    process_pool = []
    results_queue = Queue()
    ready_mem = SharedMemory(name=READY_MEM_NAME, create=True, size=READY_MEM_SIZE)

    for cam in file.cams:
        cam_proc = Process(
            target=process_main,
            args=(
                results_queue,
                cam.path,
                file.test_time,
                cam.stream_format,
                cam.resolution,
                cam.framerate
            )
        )
        cam_proc.start()

        process_pool.append(cam_proc)
    
    for _ in process_pool:
        results_queue.get()
    ready_mem.buf[0] = 1
    
    for _ in process_pool:
        cols.append(results_queue.get())

    file = sys.stdout if output == '-' else open(output, 'w')

    df = pd.DataFrame(cols)
    df = df.transpose()
    df.to_csv(file, index=False)

    ready_mem.unlink()
    results_queue.close()


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
