from calib import Calibrator
import glob
import cv2
from cv2 import aruco


if __name__ == '__main__':
    aruco_dict = aruco.Dictionary_get(cv2.aruco.DICT_4X4_100)
    board = aruco.CharucoBoard_create(8, 5, 3.5, 2.6, aruco_dict)

    obj = Calibrator(board, aruco_dict)

    images = glob.glob(r'calib_photos/*.jpg')
    print(f'Number of images: {len(images)}')
    all_corners, all_ids, img_size = obj.read_chessboards(images)
    print(f'Number of selected images: {len(all_ids)}')
    ret, mtx, dist, rvecs, tvecs = obj.calibrate_camera(all_corners, all_ids, img_size)
    print(ret)
    print(" ")
    print(mtx)
    print(" ")
    print(dist)