import cv2
import time
from utils import parse_results, request_service

def main():
    # load image
    file_name = 'pose1.jpg'
    image = cv2.imread('./assets/images/' + file_name)
    response = request_service('https://mscv.yale.edu/api', 'duke_drone_1', 'single_image', ['pose'], time.time(), image)
    print(response)

    image = parse_results(image, response['results'])
    cv2.imwrite('./assets/outputs/res_' + file_name, image)

if __name__ == "__main__":
    main()