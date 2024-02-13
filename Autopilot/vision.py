import cv2
import cv2.aruco as aruco
import numpy as np
import time
from API import *
from client import Client
from move2 import clamp2

def clamp(angle):
    angle = angle % (2*np.pi)
    if angle > np.pi:
        angle -= 2*np.pi
    return angle

class Vision :
    def __init__(self) :
        self.liste_aruco=[]



    def mainloop(self, client):


        client.handshake()
        VideoCap = False
        cap = cv2.VideoCapture(0)
        #cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)
        #cap.set(cv2.CAP_PROP_EXPOSURE, -6)
        dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
        parameters = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(dictionary, parameters)
        self.liste_aruco=[]

        # Nos valeurs de calibration
        donnees=np.load("src/calibration_params2.npz")
        mtx = cameraMatrix = donnees['cameraMatrix']
        dist = donnees['distCoeffs']
        marker_size = 0.05

        while True:
            ret, frame = cap.read()
            gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(frame)
            if markerIds is not None :
                for i in range(len(markerIds)):
                    marker_points = np.array([[-marker_size/2, marker_size/2, 0],
                                            [marker_size/2, marker_size/2, 0],
                                            [marker_size/2, -marker_size/2, 0],
                                            [-marker_size/2, -marker_size/2, 0]], dtype=np.float32)
                
                    a, rvec, tvec = cv2.solvePnP(marker_points, markerCorners[i], cameraMatrix, dist, False, cv2.SOLVEPNP_IPPE_SQUARE)
                    theta = - np.arctan((tvec[0][0]) / tvec[2][0]) # Angle avec la caméra
                    phi = rvec[2][0] + np.pi # Orientation capteur

                    robot_position = client.robots_positions[1]
                    x_robot, y_robot, theta_robot = robot_position.x, robot_position.y, robot_position.angle

                    print("robot",x_robot,y_robot,theta_robot)

                    vec_pos_robot = np.array([y_robot, x_robot])
                    vec_pos_robot.reshape(-1, 1)
                    vec_pos = np.array([tvec[2][0], tvec[0][0]])
                    vec_pos.reshape(-1, 1)

                    theta_rot = - theta_robot - theta
                    M_rot = np.array([[np.cos(theta_rot), -np.sin(theta_rot)], [np.sin(theta_rot), np.cos(theta_rot)]]).T
                    vec_pos_marqueur = M_rot.dot(vec_pos) + vec_pos_robot
                    vec_pos_marqueur.reshape(1, 2)
                    y_marqueur, x_marqueur = vec_pos_marqueur
                    theta_marqueur = phi + theta_robot
                        #self.liste_aruco.append((distance,theta,phi,markerIds[i][0]))
                    position = Position(x_marqueur,y_marqueur,clamp(theta_marqueur))
                    if is_valid_marker_id(markerIds[i][0]) or is_valid_robot_id(markerIds[i][0]):
                        client.send(Marker.Post(markerIds[i][0],position))
                        print(x_marqueur,y_marqueur,clamp(theta_marqueur),markerIds[i][0])
                        time.sleep(1)
                    
            #print(self.liste_aruco)




            

if __name__ == "__main__" :
     objVision=Vision()
     objVision.mainloop(Client(1))
