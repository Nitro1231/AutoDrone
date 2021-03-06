import cv2
import numpy as np

CAM_LEFT = 1
CAM_RIGHT = 2

CAM_HEIGHT = 420
CAM_WIDTH = 420

cam_left = cv2.VideoCapture(CAM_LEFT,  cv2.CAP_DSHOW)
cam_left.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)
cam_left.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)

cam_right = cv2.VideoCapture(CAM_RIGHT,  cv2.CAP_DSHOW)
cam_right.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)
cam_right.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)


if not (cam_left.isOpened() and cam_right.isOpened()):
    print('Cannot open camera')
    exit()


while True:
    ret_left, frame_left = cam_left.read()
    ret_right, frame_right = cam_right.read()

    gray_left = cv2.cvtColor(frame_left, cv2.COLOR_BGR2GRAY)
    gray_right = cv2.cvtColor(frame_right, cv2.COLOR_BGR2GRAY)

    if not (ret_left and ret_right):
        print('Can\'t receive frame (stream end?). Exiting ...')
        break

    stereo = cv2.StereoBM_create(numDisparities=0, blockSize=33)
    disparity = stereo.compute(gray_left, gray_right)

    local_max = disparity.max()
    local_min = disparity.min()
    disparity_grayscale = (disparity-local_min)*(65535.0/(local_max-local_min))
    disparity_fixtype = cv2.convertScaleAbs(disparity_grayscale, alpha=(255.0/65535.0))
    disparity_color = cv2.applyColorMap(disparity_fixtype, cv2.COLORMAP_JET)

    cv2.imshow('Left', gray_left)
    cv2.imshow('Right', gray_right)
    cv2.imshow('Depth map', disparity_color)

    if cv2.waitKey(1) == ord('q'):
        break


cam_left.release()
cam_right.release()
cv2.destroyAllWindows()
