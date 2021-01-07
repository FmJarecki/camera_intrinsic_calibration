import cv2
import numpy as np


class Calibrator:
    def __init__(self, board, aruco_dict):
        self.__board = board
        self.__aruco_dict = aruco_dict

    def read_chessboards(self, images):
        print("POSE ESTIMATION STARTS:")
        all_corners = []
        all_ids = []
        decimator = 0
        # SUB PIXEL CORNER DETECTION CRITERION
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.00001)

        for im in images:
            print("=> Processing image {0}".format(im))
            frame = cv2.imread(im)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            corners, ids, rejected_img_points = cv2.aruco.detectMarkers(gray, self.__aruco_dict)

            if len(corners) > 0:
                # SUB PIXEL DETECTION
                for corner in corners:
                    cv2.cornerSubPix(gray, corner,
                                     winSize=(3, 3),
                                     zeroZone=(-1, -1),
                                     criteria=criteria)
                res2 = cv2.aruco.interpolateCornersCharuco(corners, ids, gray, self.__board)
                if res2[1] is not None and res2[2] is not None and len(res2[1]) > 3 and decimator % 1 == 0:
                    all_corners.append(res2[1])
                    all_ids.append(res2[2])

            decimator += 1

        img_size = gray.shape
        return all_corners, all_ids, img_size

    def calibrate_camera(self, all_corners, all_ids, img_size):
        print("CAMERA CALIBRATION")
        flags = cv2.CALIB_FIX_K3

        (ret, camera_matrix, distortion_coefficients0,
         rotation_vectors, translation_vectors) = cv2.aruco.calibrateCameraCharuco(
                          charucoCorners=all_corners,
                          charucoIds=all_ids,
                          board=self.__board,
                          imageSize=img_size,
                          cameraMatrix=None,
                          distCoeffs=None,
                          flags=flags)

        return ret, camera_matrix, distortion_coefficients0, rotation_vectors, translation_vectors


