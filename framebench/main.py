from .list import list_cams

import fire


def main():
    fire.Fire({
        "list": list_cams
    })
