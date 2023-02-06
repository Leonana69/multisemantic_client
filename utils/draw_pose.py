import cv2

def draw_pose_keypoints(image, keypoints):
    height = image.shape[0]
    width = image.shape[1]
    for p in keypoints:
        cv2.circle(image, (int(width * p[1]), int(height * p[0])), 2, (255, 0, 0), 2)
    return image