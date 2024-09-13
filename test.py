# %%
import math
from copwrap import *
# %%
# 创建机器人实例
my_robot = Robot('/Xmate3')
# %%
joints = my_robot.get_joints()
joint_name = joints[1]
joint = my_robot.get_joint(joint_name)
print(joint.get_type())
# %%
vel = 110 * math.pi / 180
accel = 40 * math.pi / 180
jerk = 80 * math.pi / 180
config = {'maxVel': vel, 'maxAccel': accel, 'maxJerk': jerk}
# 移动某个关节
my_robot.move_joint(joint_name, 1.5, config) # target是弧度制，表示当前关节的旋转，考虑本项目的机器人都是旋转关节，没有配置其他api
# %%
sim_time = 10
sim.setStepping(True)
sim.startSimulation()
while (t := sim.getSimulationTime()) < sim_time:
    sim.step()
    print(joint.get_target_position(), joint.get_actual_position())
    joint.update()

sim.stopSimulation()