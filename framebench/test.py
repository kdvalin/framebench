import ffmpeg
import tempfile

class CameraTest:
    def __init__(self, device: str, test_time: int = 30, input_format="mjpeg", resolution="640x480", framerate=10):
        (width, _, height) = resolution.partition('x')
        self.out_tmp = tempfile.mkstemp(suffix=".mkv", prefix=f"framebench-{device.replace('/', '_')}")
        self.stream = ffmpeg.overwrite_output(
            ffmpeg
            .input(
                device,
                r=framerate,
                framerate=framerate,
                input_format=input_format,
                video_size=(width, height)
            )
            .output(self.out_tmp[1], codec="copy", t=test_time)
        )

    def run(self):
        print(ffmpeg.compile(self.stream))
        self.stream.run()