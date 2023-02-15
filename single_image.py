import json
import cv2
import numpy as np
import requests

from utils import load_image, parse_results, request_service

HOST, PORT = 'localhost', 50001

def main():
    # load image
    image = load_image('./assets/images/pose2.jpg')

    results = request_service('https://mscv.yale.edu/api', 'guojun', 'single_image', ['pose'], image)
    print(results)
    image = parse_results(image, results) # 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
    cv2.imwrite('./assets/outputs/pose2_res.jpg', image)

if __name__ == "__main__":
    main()
    