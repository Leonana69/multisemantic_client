import json
import cv2
import numpy as np
import requests

from utils import request_service, parse_results

HOST, PORT = 'localhost', 50001

def main():
    # 0 for windows, 1 for macOS
    vid = cv2.VideoCapture(1)
    while vid.isOpened():
        # Capture the video frame by frame
        ret, frame = vid.read()
        # Display the resulting frame
        if ret:
            frame = cv2.resize(frame, (480, 360), interpolation=cv2.INTER_AREA)
            results = request_service('172.29.249.77:50001/api', 'guojun', 'single_image', ['slam'], frame)
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

if __name__ == "__main__":
    main()
    