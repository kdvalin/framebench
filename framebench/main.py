from .list import list_cams
from .run import run

import fire


def main():
    fire.Fire({
        "list": list_cams,
        "run": run
    })
