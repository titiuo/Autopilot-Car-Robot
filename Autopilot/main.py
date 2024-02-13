import threading
import vision
from API import *
from client import Client
from move import *
import time

stop=0.1
robot_id=1

def mainloop(client):
    objVision=vision.Vision()
    visionthread=threading.Thread(target=objVision.mainloop,args=(client,))
    visionthread.start()
    i=2
    while True:
    #### R1 SETUP ####
        if client.state == "r1_setup" :
            d= distance(client.robots_positions[robot_id],client.markers_positions[1])
            move(clamp(d/1,1,0),get_delta_angle(client.robots_positions[robot_id],client.markers_positions[1]))
            if d<stop:
                client.send(Logic.Milestone("reached_target"))
                break
    
    ### POSITION ###
        elif client.state == "position_pair":
            theta = get_delta_angle(client.robots_positions[robot_id],client.markers_positions[i])
            move(50,theta)
            if np.abs(theta)<np.pi/8:
                client.send(Logic.Milestone("reached_target"))
                move(0,0)
                i=4
                break
    
    ### PAIR TOUR 1 ###
        elif client.state == "pair_tour_1":
            d= distance(client.robots_positions[robot_id],client.markers_positions[3])
            move(clamp(d/1,1,0),get_delta_angle(client.robots_positions[robot_id],client.markers_positions[3]))
            if d<stop:
                client.send(Logic.Milestone("reached_target"))
                break

    ### PAIR TOUR 2 ###
        elif client.state == "pair_tour_2":
            d= distance(client.robots_positions[robot_id],client.markers_positions[5])
            move(clamp(d/1,1,0),get_delta_angle(client.robots_positions[robot_id],client.markers_positions[5]))
            if d<stop:
                client.send(Logic.Milestone("reached_target"))
                break
        else:
            move(0,0)
            time.sleep(0.1)
            pass


    # objtest=test.test()
    # print(objtest.test)
    # testthread=threading.Thread(target=objtest.mainloop,args=())
    # testthread.start()
    # print(objtest.test)


    

if __name__=='__main__':
    mainloop(Client(1))






