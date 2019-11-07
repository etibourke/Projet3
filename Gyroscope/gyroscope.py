#This code as been taken from a youtube video at this link : https://www.youtube.com/watch?v=FJf0lB9HAD0&t=206s

import MPU6050
import time

mpu = MPU6050.MPU6050()
accel = [0]*3
gyro = [0]*3
def setup():
    mpu.dmp_initialize()

def recordGyro():
    while(True):
        accel = mpu.get_acceleration()
        gyro = mpu.get_rotation()
        print("a/g:%d/t%d/t%d/t%d/t%d/t%d "%(accel[0],accel[1],accel[2],gyro[0],gyro[1],gyro[2]))
        print("a/g:%.2f g\t%.2f g\t%.2f g\t%.2f d/s\t%.2f d/s\t%.2f d/s"%(accel[0]/16384.0,accel[1]/16384.0,accel[2]/16384.0,gyro[0]/131.0,gyro[1]/131.0,gyro[2]/131.0))
        time.sleep(0.1)

if __name__ == '__main__' :
    print("Program is starting ...")
    setup()
    try:
        recordGyro()
    except KeyboardInterrupt:
        pass
