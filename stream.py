import json
import cv2
import numpy as np
import requests

from utils.draw_pose import draw_pose_keypoints

HOST, PORT = 'localhost', 50001

def load_image(path):
    image = cv2.imread(path)
    return image

def encode_as_list(img):
    [ret, encoded_image] = cv2.imencode('.jpg', img)
    if ret:
        np_image = np.array(encoded_image)
        print('[M] encode [SUCCESS]')
        return np_image.tolist()
    else:
        print('[M] encode [FAILED]')
        return []

def request_service(user, mode, function, image):
    packet = {
        'user': user,
        'mode': mode,
        'function': function,
        'image': encode_as_list(image)
    }

    # send POST
    headers = {'Content-type': 'application/json'}
    r = requests.post('http://localhost:50001/api', data=json.dumps(packet), headers=headers)
    # print result
    print('status: ', r.json()['status'])
    return r.json()['result']

def parse_results(image, results):
    for r in results:
        if r['function'] == 'pose':
            image = draw_pose_keypoints(image, np.array(r['output']))
        else:
            print('[M] function not supported')
    return image

def main():
    # 0 for windows, 1 for macOS
    vid = cv2.VideoCapture(1)
    while vid.isOpened():
        # Capture the video frame by frame
        ret, frame = vid.read()
        # Display the resulting frame
        if ret:
            frame = cv2.resize(frame, (480, 270), interpolation=cv2.INTER_AREA)
            results = request_service('guojun', 'single-image', ['pose'], frame)
            image = parse_results(frame, results)
            cv2.imshow('frame', frame)
            # press 'q' to break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
  
    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()
    return

    

    # load image
    image = load_image('./assets/images/pose1.jpg')

    packet = {
        'user': 'guojun',
        'mode': 'single-image',
        'function': ['pose'],
        'image': encode_as_list(image)
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
    