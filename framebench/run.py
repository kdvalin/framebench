import time

import cv2
from PIL import Image
import hashlib


def run(device: str, test_time: int = 30):
    """Run benchmark with the provided device

    :param device: The video device which will be used.
    :param time: The time (in seconds) to run the benchmark for.
    """
    timings = []
    vid = cv2.VideoCapture(device)
    vid.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', "J", "P", "G"))
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    print(f"{vid.get(cv2.CAP_PROP_FRAME_WIDTH)}x{vid.get(cv2.CAP_PROP_FRAME_HEIGHT)} @ {vid.get(cv2.CAP_PROP_FPS)} fps using {hex(int(vid.get(cv2.CAP_PROP_FOURCC)))}")

    while not vid.isOpened(): # Wait for cam to open before tagging a start time
        pass
    start_time = time.time()

    last_frame = (None, start_time) #checksum, time
    while time.time() - start_time < test_time:
        ret, frame = vid.read()
        frame_time = time.time()

        if not ret:
            print("Can't receive frame (stream end?).")
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
    print(','.join([str(i) for i in timings[1:]]))