import datetime as dt

import cv2
from PIL import Image
import hashlib

def run(device: str, time: int = 30):
    """Run benchmark with the provided device

    :param device: The video device which will be used.
    :param time: The time (in seconds) to run the benchmark for.
    """
    timings = []
    vid = cv2.VideoCapture(device)

    while not vid.isOpened(): # Wait for cam to open before tagging a start time
        pass
    start_time = dt.datetime.now()

    last_frame_cksum = (None, dt.datetime.now())
    while (dt.datetime.now() - start_time).total_seconds() < time:
        ret, frame = vid.read()
        frame_time = dt.datetime.now()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?).")
            continue
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(frame)
        pil_chksum = hashlib.sha256(im_pil.tobytes())

        if pil_chksum != last_frame_cksum[0]: #New frame
            timings.append((frame_time - last_frame_cksum[1]).microseconds/1e3)
            last_frame_cksum = (pil_chksum, frame_time)
        
    vid.release()
    print(','.join([str(i) for i in timings[1:]]))