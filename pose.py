import cv2
import time
from utils import encode_as_string, parse_results, request_service

def main():
    # load image
    file_name = 'pose1.jpg'
    image = cv2.imread('./assets/images/' + file_name)
    data = {
        'image': {
            'format': 'default',
            'content': encode_as_string(image)
        }
    }
    response = request_service('https://mscv.yale.edu/api', 'duke-drone-1', 'image', ['pose'], time.time(), data)
    print(response)

    image = parse_results(image, response['results'])
    cv2.imwrite('./assets/outputs/res_' + file_name, image)

if __name__ == "__main__":
    main()