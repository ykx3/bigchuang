from .globals import sim
from .joint import Joint


class Robot:
    def __init__(self, robot_root_path):
        """
        初始化机器人类。

        :param robot_root_path: 机器人根节点的路径
        """
        self.root_handle = sim.getObject(robot_root_path)
        self.joints = {}  # 存储关节的字典

        # 获取所有关节
        self._get_all_joints(self.root_handle)

    def _get_all_joints(self, handle):
        """
        递归获取所有关节。

        :param handle: 当前对象的句柄
        """
        if sim.isHandle(handle):  # 检查是否是有效的句柄
            # 获取当前对象的所有子对象
            children = sim.getObjectsInTree(handle, sim.object_joint_type)

            for child in children:
                # 如果是关节，添加到字典中
                joint = Joint(handle=child)
                self.joints[joint.get_name()] = joint
                # print(f"Found joint: {joint.get_name()}")
        else:
            raise Exception('Not a handle: {}'.format(handle))

    def get_joint(self, name) -> Joint:
        """
        根据名称获取关节。

        :param name: 关节的名称
        :return: Joint对象
        """
        return self.joints.get(name)

    def move_joint(self, name, target_position):
        """
        移动指定关节到目标位置。

        :param name: 关节的名称
        :param target_position: 目标位置
        """
        joint = self.get_joint(name)
        if joint:
            joint.set_target_position(target_position)
        else:
            raise Exception('No such joint named {}'.format(name))

    def update_joints(self):
        """
        更新所有关节的状态信息。
        """
        for joint in self.joints.values():
            joint.update()
