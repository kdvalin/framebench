import cv2
import argparse
import fire

def list_cams():
    print("hit")


def main():
    fire.Fire({
        "list": list_cams
    })
