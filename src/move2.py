from PCA9685 import PCA9685
import time
import moteur 
import numpy as np
from API import *

Motor = moteur.MotorDriver()

def move(speed,angle):
    '''
    speed entre 0 et 1
    angle entre -pi et pi
    '''
    angle=angle/np.pi
    left=max(min(2-np.abs(4*angle+1),1),-1)
    right=max(min(2-np.abs(4*angle-1),1),-1)
    
    fr='forward'
    fl='forward'
    if left<0:
        fl='backward'
    if right<0:
        fr='backward'   

    Motor.MotorRun(0,fl, speed*np.abs(left)*100)
    Motor.MotorRun(1,fr, speed*np.abs(right)*100)


def get_delta_angle(ma_pos:Position,target_pos:Position):
    angle = np.arctan2(target_pos.y-ma_pos.y, target_pos.x-ma_pos.x) - ma_pos.angle
    while abs(angle)>2*np.pi:
        if angle>0:
            angle -= 2*np.pi
        else:
            angle += 2*np.pi
    return angle

def distance(ma_pos:Position,target_pos:Position):
    return np.sqrt((ma_pos.x-target_pos.x)**2+(ma_pos.y-target_pos.y)**2)

def clamp(d,a,b):
    return max(min(d,b),a)

def clamp2(angle):
    while abs(angle)>2*np.pi:
        if angle>0:
            angle -= 2*np.pi
        else:
            angle += 2*np.pi
    return angle