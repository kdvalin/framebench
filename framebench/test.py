import ffmpeg
import tempfile

class CameraTest:
    def __init__(self, device: str):
        self.out_tmp = tempfile.mkstemp(suffix=".mkv", prefix=f"framebench-{device.replace('/', '_')}")
        self.stream = ffmpeg.input(device).output(self.out_tmp[1])
    
    def run(self):
        self.stream.run()