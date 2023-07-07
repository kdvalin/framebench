from distutils.core import setup

setup(
    name="FrameBench",
    description="A Benchmark for measuring frame timings from multiple cameras simultaneously",
    version="1.0.0",
    author="Keith Valin",
    author_email="kvalin@redhat.com",
    install_requires = [
        "opencv-python",
        "fire"
    ],
    entry_points = {
        "console_scripts": [
            "framebench = framebench.main:main"
        ]
    }
)