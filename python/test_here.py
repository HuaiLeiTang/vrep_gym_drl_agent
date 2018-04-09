import vrep
import sys
import math

vrep.simxFinish(-1)
__clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)  # Connect to V-REP
if __clientID == -1:
    print('Failed connecting to remote API server')
    sys.exit()


def getHandle(name):
    code, handle = vrep.simxGetObjectHandle(__clientID, name, vrep.simx_opmode_blocking)
    vrep.sim_vis
    if code == 0:
        return handle
    else:
        print('Error code ', code, ' was returned! Please check!')
        sys.exit()


fl_brake_handle = getHandle('joint_front_left_wheel')
fr_brake_handle = getHandle('joint_front_right_wheel')
bl_brake_handle = getHandle('joint_back_left_wheel')
br_brake_handle = getHandle('joint_back_right_wheel')


def rotations(handle, direction, strength=40.0):
    director = 1.0
    if handle in {fl_brake_handle, bl_brake_handle}:
        director = -1.0
    if direction == 1:
        director *= -1.0
    elif direction == -1:
        director *= 1.0
    else:
        print('Invalid Direction')
        sys.exit()
    return strength * math.pi / (180.0 * director)


vrep.simxSetJointTargetVelocity(__clientID, fl_handle, rotations(fl_handle, 1), vrep.simx_opmode_oneshot)
vrep.simxSetJointTargetVelocity(__clientID, fr_handle, rotations(fr_handle, 1), vrep.simx_opmode_oneshot)
vrep.simxSetJointTargetVelocity(__clientID, bl_handle, rotations(bl_handle, -1), vrep.simx_opmode_oneshot)
vrep.simxSetJointTargetVelocity(__clientID, br_handle, rotations(br_handle, -1), vrep.simx_opmode_oneshot)

# vrep.simxFinish(-1)
