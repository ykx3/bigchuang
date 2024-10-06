import time
import matplotlib.pyplot as plt
import numpy as np

from camera import RGBDCamera

camera = RGBDCamera()
color, depth = camera.get_frame()
if color is not None:
    plt.imshow(color)
    plt.show()
if depth is not None:
    plt.imshow(depth)
    plt.show()
# cnt = 0
# start = time.time()
# for i in range(10):
#     a, b = camera.get_frame()
#     cnt += a is None or b is None
# end = time.time()
# print(cnt)
# print(end - start)
from camera.utils import *

pcd = rgbd2cloud(depth, color, **camera.get_para())


def create_coordinate_frame(size=1.0):
    # 创建坐标轴
    points = [
        [0, 0, 0], [size, 0, 0], [0, size, 0], [0, 0, size]
    ]
    lines = [
        [0, 1], [0, 2], [0, 3]  # 连接原点到每个轴的方向
    ]
    colors = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]  # RGB颜色，分别对应XYZ轴

    line_set = o3d.geometry.LineSet()
    line_set.points = o3d.utility.Vector3dVector(points)
    line_set.lines = o3d.utility.Vector2iVector(lines)
    line_set.colors = o3d.utility.Vector3dVector(colors)

    return line_set


def add_origin_marker(size=0.1):
    # 创建原点标记，这里用一个小球体表示
    mesh_sphere = o3d.geometry.TriangleMesh.create_sphere(radius=size)
    mesh_sphere.paint_uniform_color([1, 0.706, 0])  # 设置颜色
    mesh_sphere.translate((0, 0, 0))  # 移动到原点
    return mesh_sphere


# 创建坐标轴
coordinate_frame = create_coordinate_frame()

# 创建原点标记
origin_marker = add_origin_marker()

m = np.eye(4)
# m[:3, :3] = get_rotation_matrix('x', np.pi)
pcd.transform(m)
visualize_pcd(pcd, coordinate_frame, origin_marker)
