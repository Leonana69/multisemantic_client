import cv2
import numpy as np
import requests, json

def draw_pose_keypoints(image, keypoints):
    height = image.shape[0]
    width = image.shape[1]
    for p in keypoints:
        cv2.circle(image, (int(width * p[1]), int(height * p[0])), 2, (255, 0, 0), 2)
    return image

def encode_as_list(img):
    if img is None:
        print('[M] encode None')
        return []
    [ret, encoded_image] = cv2.imencode('.jpg', img)
    if ret:
        np_image = np.array(encoded_image)
        print('[M] encode [SUCCESS]')
        return np_image.tolist()
    else:
        print('[M] encode [FAILED]')
        return []

def request_service(url, user, mode, function, image):
    packet = {
        'user': user,
        'mode': mode,
        'index': 1,
        'function': function,
        'image': {
            'format': 'cv_compressed',
            'data': encode_as_list(image)
        }
    }

    if image is None:
        packet['image'] = {
            'format': 'none',
            'data': []
        }

    # send POST
    headers = {'Content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(packet), headers=headers)
    # print message
    # print('message:', r.json()['msg'])
    print('message:', r.json())
    return r.json()['result']

def parse_results(image, results):
    for r in results:
        if r['function'] == 'pose':
            image = draw_pose_keypoints(image, np.array(r['output']))
        elif r['function'] == 'slam':
            pass
        else:
            print('[M] function not supported')
    return image

def load_image(path):
    image = cv2.imread(path)
    return image