import json
import cv2
import numpy as np
import requests

def draw_pose_keypoints(image, keypoints):
    height = image.shape[0]
    width = image.shape[1]
    for p in keypoints:
        cv2.circle(image, (int(width * p[1]), int(height * p[0])), 2, (255, 0, 0), 2)
    return image

def load_image(path):
    image = cv2.imread(path)
    return image

def main():
    HOST, PORT = 'localhost', 50001

    # load image
    image = load_image('./assets/images/pose1.jpg')

    # this is not the best compression
    [rslt, encoded_image] = cv2.imencode('.jpg', image)
    np_image = np.array(encoded_image)

    packet = {
        'user': 'guojun',
        'mode': 'single-image',
        'function': ['pose'],
        'image': np_image.tolist()
    }

    json_packet = json.dumps(packet)

    # send POST
    headers = {'Content-type': 'application/json'}
    r = requests.post('http://localhost:50001/api', data=json_packet, headers=headers)
    # save result
    print(r.json())
    result = np.array(r.json()['result'][0]['output'])
    marked_image = draw_pose_keypoints(image, result)
    cv2.imwrite('./assets/outputs/res1.jpg', marked_image)

if __name__ == "__main__":
    main()
    