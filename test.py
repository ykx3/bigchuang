# %%
from copwrap import *
# %%
# 创建机器人实例
my_robot = Robot('/Xmate3')
# %%
joint_name = 'Xmate3_joint2'
joint = my_robot.get_joint(joint_name)
print(joint.get_type())
# 移动某个关节
my_robot.move_joint(joint_name, 0.1)
# %%
sim_time = 5
sim.setStepping(True)
sim.startSimulation()
while (t := sim.getSimulationTime()) < sim_time:
    sim.step()
    print(joint.get_position(), joint.get_orientation())
    my_robot.move_joint(joint_name, t * 0.1)
    # sim.setJointPosition(joint.joint_handle, 0.01)
    joint.update()

sim.stopSimulation()