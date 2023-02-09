import json
import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
import parse

from utils import request_service, parse_results

HOST, PORT = 'localhost', 50001

position_x = []
position_y = []
position_z = []
orientation = []
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim3d([-1.0, 1.0])
ax.set_xlabel('x')
ax.set_ylim3d([-1.0, 1.0])
ax.set_ylabel('y')
ax.set_zlim3d([-1.0, 1.0])
ax.set_zlabel('z')

def parse_msg(str_msg):
    lines = str_msg.split('\n')
    for idx in range(0, len(lines)):
        if lines[idx] == 'pose: ':
            position_x.append(float(lines[idx + 2].split()[1]))
            position_y.append(float(lines[idx + 3].split()[1]))
            position_z.append(float(lines[idx + 4].split()[1]))
            ox = float(lines[idx + 6].split()[1])
            oy = float(lines[idx + 7].split()[1])
            oz = float(lines[idx + 8].split()[1])
            orientation.append(np.array([ox, oy, oz]))
            break

def plot(i):
    ax.clear()
    x = np.array(position_x)
    y = np.array(position_y)
    z = np.array(position_z)
    ax.scatter(x, y, z)

def main():
    # 0 for windows, 1 for macOS
    vid = cv2.VideoCapture(1)

    anim = animation.FuncAnimation(fig, plot, interval=100)
    plt.show(block=False)
    
    while vid.isOpened():
        # Capture the video frame by frame
        ret, frame = vid.read()
        # Display the resulting frame
        if ret:
            frame = cv2.resize(frame, (480, 360), interpolation=cv2.INTER_AREA)
            results = request_service('http://172.29.249.77:50001/api', 'guojun', 'stream', ['slam'], frame)
            # image = parse_results(frame, results)
            
            if len(results) > 0:
                msg = results[0]['output']
                if len(msg) > 0:
                    parse_msg(msg[0])

            cv2.imshow('frame', frame)
            # press 'q' to break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                # print(position_x)
                # print(orientation)
                break
  
    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()
    return

if __name__ == "__main__":
    main()
    