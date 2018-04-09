from LIDAR import Lidar
import numpy as np
import gym
import driver
from gym import spaces
import cv2
import math


class Tracker(gym.Env):
    def __init__(self, headless=False):
        # self.venv = vrepper(headless=headless,dir_vrep='C:\Program Files\V-REP3\V-REP_PRO_EDU\\')
        driver.initiate()
        driver.startSimulation()
        self._lidar = Lidar()
        self.lidar_obs = self.__getLidarPicture()
        self.action_funcs = [self.__forward, self.__backward, self.__right_fwd, self.__right_bkw, self.__left_fwd, self.__left_bkw]
        self._velocity = 2*math.pi
        self._torque = 60
        self.action_space = spaces.Discrete(6)
        self.observation_space = spaces.Box(np.zeros((96,)), np.ones((96,)))

    def __forward(self):
        driver.setMotorVelocity(self._velocity, self._torque)

    def __backward(self):
        driver.setMotorVelocity((-1) * self._velocity, self._torque)

    def __right_fwd(self):
        driver.setMotorVelocity(self._velocity, self._torque)
        driver.setSteeringAngle(0.5235987)

    def __left_fwd(self):
        driver.setMotorVelocity(self._velocity, self._torque)
        driver.setSteeringAngle(-0.5235987)

    def __right_bkw(self):
        driver.setMotorVelocity((-1) * self._velocity, self._torque)
        driver.setSteeringAngle(0.5235987)

    def __left_bkw(self):
        driver.setMotorVelocity((-1) * self._velocity, self._torque)
        driver.setSteeringAngle(-0.5235987)



    def _self_observe(self):
        self.observation = np.array(self.__getLidarPicture()).astype('float32')

    def _step(self, actions):
        assert self.action_space.contains(actions)
        v = actions
        self.action_funcs[v]()
        driver.takeStep()
        self._self_observe()

        return self.observation, 0, False, {}

    def _render(self, mode='human', close=False):
        if close:
            cv2.destroyAllWindows()
            return

        im = self.observation
        cv2.imshow('render', im)
        cv2.waitKey(1)

    def _reset(self):
        driver.stopSimulation()
        driver.startSimulation()
        driver.setMotorVelocity(0, 0)
        self._self_observe()
        return self.observation

    def _destroy(self):
        driver.stopSimulation()
        driver.cleanUp()

    def __getLidarPicture(self):
        return self._lidar.getReading()

    def close(self):
        driver.stopSimulation()
        driver.cleanUp()
