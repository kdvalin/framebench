from .consts import READY_MEM_NAME, READY_MEM_SIZE

import tempfile
import logging
import json
import os
import time


from multiprocessing.shared_memory import SharedMemory
from multiprocessing import Queue

import ffmpeg


def process_main(queue: Queue, device: str, test_time: int = 30, input_format="mjpeg", resolution="640x480", framerate=30):
    mem = SharedMemory(name=READY_MEM_NAME, create=False, size=READY_MEM_SIZE)
    test = CameraTest(device, test_time, input_format, resolution, framerate)
    
    queue.put('ready')
    while mem.buf[0] != 1:
        time.sleep(0.066)
    mem.close()

    test.run()
    
    queue.put(test.get_results())

    test.cleanup()


class CameraTest:
    def __init__(self, device: str, test_time: int = 30, input_format="mjpeg", resolution="640x480", framerate=30):
        self.output = [device]
        self.logger = logging.getLogger(__package__)
        (width, _, height) = resolution.partition('x')

        self.out_tmp = tempfile.mkstemp(suffix=".mkv", prefix=f"framebench-{device.replace('/', '_')}")[1]
        self.stream = ffmpeg.overwrite_output(
            ffmpeg
            .input(
                device,
                r=framerate,
                framerate=framerate,
                input_format=input_format,
                video_size=(width, height),
                loglevel="error"
            )
            .output(self.out_tmp, codec="copy", t=test_time)
        )

        self.logger.info(f"Opened {device} at {resolution} targeting {framerate}fps ({input_format})")

    def run(self):
        self.logger.debug(ffmpeg.compile(self.stream))
        self.stream.run()

    def get_results(self):
        file_results = ffmpeg.probe(
            self.out_tmp,
            loglevel="error",
            select_streams="v:0",
            show_entries="packet=pts_time",
        )
        last = None
        for time in file_results['packets']:
            current = float(time['pts_time'])
            if last is not None:
                self.output.append(current - last)
            last = current

        return self.output

    def cleanup(self):
        os.unlink(self.out_tmp)
