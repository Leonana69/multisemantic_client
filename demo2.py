import cv2
import time
import numpy as np
from utils import request_service

def main():
    # 0 for windows, 1 for macOS
    vid = cv2.VideoCapture('/Users/guojun/Workspace/data/server_slam/drone_nuc/video/nuc.mp4')

    # use 'duke_drone_1' or 'duke_drone_2' here for user
    user = 'duke_drone_2'
    while vid.isOpened():
        # Capture the video frame by frame
        ret, frame = vid.read()
        if ret:
            frame = cv2.resize(frame, (540, 360), interpolation=cv2.INTER_AREA)
            results = request_service('https://mscv.yale.edu/api', user, 'stream', ['slam'], time.time(), frame)
            if len(results) > 0:
                msg = results[0]['output']
                if len(msg) > 0:
                    print(msg[0])

            cv2.imshow('frame', frame)
            # press 'q' to break
            if cv2.waitKey(1) & 0xFF == ord('w'):
                break

    # results = request_service('https://mscv.yale.edu/api', user, 'stop', ['slam'], 0.0, None)

    vid.release()
    cv2.destroyAllWindows()
    return

if __name__ == "__main__":
    main()