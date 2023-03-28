import cv2
import numpy as np
import requests, json, base64

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
        print('[M] encode as list [SUCCESS]')
        return np_image.tolist()
    else:
        print('[M] encode [FAILED]')
        return []

def encode_as_string(img):
    if img is None:
        print('[M] encode None')
        return []
    [ret, encoded_image] = cv2.imencode('.png', img)
    if ret:
        np_bytes = np.array(encoded_image).tobytes()
        print('[M] encode as string [SUCCESS]')
        return base64.encodebytes(np_bytes).decode()
    else:
        print('[M] encode [FAILED]')
        return []

def request_service(url, user, mode, function, timestamp, image, imu=[]):
    packet = {
        'user': user,
        'mode': mode,
        'timestamp': timestamp,
        'function': function,
        'data': {
            'image': {
                'format': 'default',
                'content': encode_as_string(image)
            },
            'imu': {
                'content': imu,
            }
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
    return r.json()

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