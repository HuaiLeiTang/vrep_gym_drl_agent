import driver

class Lidar:
    def __init__(self):
        lidars = driver.lidars
        self._triangle_a = driver.getLidarSensorReading(lidars[0])[2] #vrep_env.get_object_by_name('TriangleA').get_depth_sensor()
        self._triangle_b = driver.getLidarSensorReading(lidars[1])[2] #vrep_env.get_object_by_name('TriangleB').get_depth_sensor()
        self._triangle_c = driver.getLidarSensorReading(lidars[2])[2] #vrep_env.get_object_by_name('TriangleC').get_depth_sensor()

    def getReading(self):
        sensor_data = self._triangle_b + self._triangle_a + self._triangle_c
        return sensor_data