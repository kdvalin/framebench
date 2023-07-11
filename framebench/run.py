from .models import config

import time
import hashlib
import logging
import sys
import concurrent.futures
import csv

import cv2
import yaml
import pandas as pd 
from PIL import Image


logger = logging.getLogger(__package__)

def setup_capture_device(device: str, resolution: str, framerate: int, format: str):
    (width, _, height) = resolution.partition("x")
    
    vid = cv2.VideoCapture(device)
    
    vid.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*format))
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, int(width))
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, int(height))

    if not vid.isOpened():
        raise RuntimeError(f"Could not open {device}")

    cv_resolution = f"{vid.get(cv2.CAP_PROP_FRAME_WIDTH)}x{vid.get(cv2.CAP_PROP_FRAME_HEIGHT)}"
    cv_fps = vid.get(cv2.CAP_PROP_FPS)
    cv_format = int(vid.get(cv2.CAP_PROP_FOURCC)).to_bytes(4, sys.byteorder).decode()

    logger.debug(f"Opened {device} at {cv_resolution} {cv_fps}fps using {cv_format} encoding")

    return vid


def run(device: str, test_time: int = 30, resolution="640x480", framerate=30, format="MJPG"):
    """Run benchmark with the provided device

    :param device: The video device which will be used.
    :param test_time: The time (in seconds) to run the benchmark for.
    :param resolution: The desired resolution of the camera
    :param framerate: The desired framerate of the camera
    :param format: The format to be used (must be 4 characters, use `list` to validate what is supported on a camera)
    """
    timings = []
    vid = setup_capture_device(device, resolution, framerate, format)
    start_time = time.time()

    last_frame = (None, start_time) #checksum, time
    while time.time() - start_time < test_time:
        ret, frame = vid.read()
        frame_time = time.time()

        if not ret:
            logging.warn("Can't receive frame (stream end?).")
            continue

        #OpenCV brings frames in using BGR, convert it to RGB to prevent PIL from getting confused
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(frame)
        pil_chksum = hashlib.sha1(pil_img.tobytes())
        
        if pil_chksum != last_frame[0]:
            if last_frame[0] != None: # Skip first frame, since camera initialization gives a large initial frame time
                timings.append((frame_time - last_frame[1]) * 1e3)
            last_frame = (pil_chksum, frame_time)
        
    vid.release()
    return timings

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
    