import ffmpeg
import tempfile

class CameraTest:
    def __init__(self, device: str, test_time: int = 30, input_format="mjpeg"):
        self.out_tmp = tempfile.mkstemp(suffix=".mkv", prefix=f"framebench-{device.replace('/', '_')}")
        self.stream = ffmpeg.overwrite_output(
            ffmpeg.input(device, t=test_time, input_format=input_format).output(self.out_tmp[1], codec="copy")
        )

    def run(self):
        self.stream.run()