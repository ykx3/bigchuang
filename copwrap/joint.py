from .globals import sim, SceneObjectSubTypes


class Joint:
    def __init__(self, path=None, handle=None):
        """
        初始化关节类。

        :param handle: 关节的handle
        :param path: 关节在场景中的路径
        """
        self.joint_handle = sim.getObject(path) if handle is None else handle
        self.name = sim.getObjectName(self.joint_handle)
        self.position = sim.getObjectPosition(self.joint_handle, -1)
        self.orientation = sim.getObjectOrientation(self.joint_handle, -1)
        self.target_position = sim.getJointTargetPosition(self.joint_handle)
        self.actual_position = sim.getJointPosition(self.joint_handle)
        self.type = sim.getJointType(self.joint_handle)
        self.properties = sim.getObjectProperty(self.joint_handle)

    def get_name(self):
        """获取关节的名称"""
        return self.name

    def get_position(self):
        """获取关节的位置"""
        return self.position

    def get_orientation(self):
        """获取关节的方向"""
        return self.orientation

    def get_target_position(self):
        """获取关节的目标位置"""
        return self.target_position

    def get_actual_position(self):
        """获取关节的实际位置"""
        return self.actual_position

    def get_type(self):
        """获取关节的类型"""
        return SceneObjectSubTypes[self.type]

    def get_properties(self):
        """获取关节的属性"""
        return self.properties

    def set_target_position(self, target_position):
        """
        设置关节的目标位置。

        :param target_position: 新的目标位置
        """
        sim.setJointTargetPosition(self.joint_handle, target_position)

    def update(self):
        """更新关节的状态信息"""
        self.name = sim.getObjectName(self.joint_handle)
        self.position = sim.getObjectPosition(self.joint_handle, -1)
        self.orientation = sim.getObjectOrientation(self.joint_handle, -1)
        self.target_position = sim.getJointTargetPosition(self.joint_handle)
        self.actual_position = sim.getJointPosition(self.joint_handle)
