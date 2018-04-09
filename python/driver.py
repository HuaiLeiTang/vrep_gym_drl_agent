import vrep
import sys
import time
import math
import matplotlib.pyplot as plt
import subprocess as sp

__clientID = None
lidars = None
rotor = None
inst = None
steer_handle = None

def initiate():
    global __clientID
    global lidars
    global rotor
    global inst
    global steer_handle
    port_num = 19999
    path_vrep = 'C:\Program Files\V-REP3\V-REP_PRO_EDU\\vrep'
    args = [path_vrep, '-gREMOTEAPISERVERSERVICE_' + str(port_num) + '_FALSE_TRUE']

    try:
        inst = sp.Popen(args)
    except EnvironmentError:
        print('(instance) Error: cannot find executable at', args[0])
        raise

    vrep.simxFinish(-1)
    retries = 0
    while True:
        print('(vrepper)trying to connect to server on port', port_num, 'retry:', retries)
        # vrep.simxFinish(-1) # just in case, close all opened connections
        __clientID = vrep.simxStart(
            '127.0.0.1', port_num,
            waitUntilConnected=True,
            doNotReconnectOnceDisconnected=True,
            timeOutInMs=1000,
            commThreadCycleInMs=0)  # Connect to V-REP

        if __clientID != -1:
            print('(vrepper)Connected to remote API server!')
            break
        else:
            retries += 1
            if retries > 15:
                vrep.end()
                raise RuntimeError('(vrepper)Unable to connect to V-REP after 15 retries.')

    vrep.simxLoadScene(__clientID, 'C:\Program Files\V-REP3\V-REP_PRO_EDU\scenes\\not_pristine.ttt',
                       0,  # assume file is at server side
                       vrep.simx_opmode_blocking)
    # vrep.simxFinish(-1)
    # __clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)  # Connect to V-REP
    vrep.simxSynchronous(__clientID, True)
    lidars = ['TriangleA', 'TriangleB', 'TriangleC']
    lidars = [getHandle(x) for x in lidars]
    rotor = getHandle('motor_joint')
    steer_handle = getHandle('steer_joint')


def cleanUp():
    vrep.simxFinish(-1)
    if inst.poll() is None:
        inst.terminate()


def simStep():
    vrep.simxSynchronousTrigger(__clientID)


def startSimulation():
    vrep.simxStartSimulation(__clientID, vrep.simx_opmode_blocking)
    takeStep()
    # vrep.simxSetJointTargetVelocity(__clientID, rotor, 20 * math.pi, vrep.simx_opmode_blocking)


def stopSimulation():
    vrep.simxStopSimulation(__clientID, vrep.simx_opmode_blocking)


def takeStep():
    vrep.simxSynchronousTrigger(__clientID)


def getHandle(name):
    code, handle = vrep.simxGetObjectHandle(__clientID, name, vrep.simx_opmode_blocking)
    if code == 0:
        return handle
    else:
        print('Error code ', code, ' was returned! Please check!')
        sys.exit()


def goForward():
    vrep.simxSetJointTargetVelocity(__clientID, rotor, 100, vrep.simx_opmode_blocking)

def getLidarSensorReading(handle):
    return vrep.simxGetVisionSensorDepthBuffer(__clientID, handle, vrep.simx_opmode_blocking)

def getSensorReading(sensor_name):
    return vrep.simxGetVisionSensorDepthBuffer(__clientID, getHandle(sensor_name), vrep.simx_opmode_blocking)

def initiateLidarSensors(sensors):
    return [getHandle(x) for x in sensors]


def setMotorVelocity(velocity, torque):
    vrep.simxSetJointForce(__clientID,rotor, torque, vrep.simx_opmode_blocking)
    vrep.simxSetJointTargetVelocity(__clientID, rotor, velocity, vrep.simx_opmode_blocking)

def setSteeringAngle(angle):
    vrep.simxSetJointTargetPosition(__clientID,steer_handle,angle,vrep.simx_opmode_blocking)

