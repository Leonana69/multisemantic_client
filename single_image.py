import cv2
from utils import load_image, parse_results, request_service

def main():
    # load image
    file_name = 'pose1.jpg'
    image = load_image('./assets/images/' + file_name)

    # results = request_service('https://mscv.yale.edu/api', 'duke_drone_1', 'single_image', ['pose'], 0.0, image)
    results = request_service('http://172.29.249.77:50002/api', 'duke_drone_1', 'single_image', ['pose'], 0.0, image)
    print(results)
    image = parse_results(image, results)
    cv2.imwrite('./assets/outputs/res_' + file_name, image)

if __name__ == "__main__":
    main()