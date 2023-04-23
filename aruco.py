import time, cv2
import numpy as np
from utils import encode_as_string, request_service

def main():
    img = cv2.imread('./assets/images/aruco.jpg')
    data = {
        'image': {
            'format': 'default',
            'content': encode_as_string(img)
        },
    }
    response = request_service('https://mscv.yale.edu/api', 'guojun', 'image', ['aruco'], time.time(), data)
    print(response)

if __name__ == "__main__":
    main()