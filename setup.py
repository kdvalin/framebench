from distutils.core import setup

setup(
    name="FrameBench",
    description="A Benchmark for measuring frame timings from multiple cameras simultaneously",
    version="1.0.0",
    author="Keith Valin",
    author_email="kvalin@redhat.com",
    license="GPL-3.0",
    url="https://github.com/kdvalin/framebench",
    keywords=["camera", "webcam", "framebench", "test", "benchmark", "frame timings"],
    install_requires = [
        "opencv-python",
        "fire",
        "pillow",
        "pyyaml",
        "pydantic",
        "pandas"
    ],
    entry_points = {
        "console_scripts": [
            "framebench = framebench.main:main"
        ]
    },
    classifiers=[
        "5 - Production/Stable",
        "Topic :: Benchmark :: Cameras"
        "License :: OSI Approved :: GPL3 License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8"
    ]
)