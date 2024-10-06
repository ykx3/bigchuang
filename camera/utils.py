import cv2
import numpy as np
import open3d as o3d


def read_color_image(path):
    color_image = cv2.imread(path, cv2.IMREAD_COLOR)
    color_image_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
    return color_image_rgb


def read_depth_image(path):
    depth_image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    return depth_image


def read_pcd(path):
    # Read the point cloud from file
    return o3d.io.read_point_cloud(path)


def write_color_image(path, color_image):
    cv2.imwrite(path, color_image)


def write_depth_image(path, depth_image):
    cv2.imwrite(path, depth_image)


def write_pcd(path, pcd):
    o3d.io.write_point_cloud(path, pcd)


def rgbd2cloud(depth_image, color_image, depth_scale=0.001, fx=1656, fy=1656, cx=960, cy=540, no_color=False):
    # fx, fy = 1656, 1656  # 焦距
    # cx, cy = 1920 / 2, 1080 / 2  # 主点

    # 将深度图像转换为点云
    height, width = depth_image.shape
    xx, yy = np.meshgrid(np.arange(width), np.arange(height))
    valid = depth_image > 0
    z = depth_image[valid] * depth_scale
    x = (xx[valid] - cx) * z / fx
    y = (yy[valid] - cy) * z / fy
    # points = np.vstack((z, -x, -y)).transpose()
    points = np.vstack((x, y, z)).transpose()

    # 使用Open3D创建带有颜色的点云对象
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    # 提取对应的颜色信息
    if not no_color:
        colors = color_image[valid] / 255.0  # 归一化颜色值到 [0, 1]
        pcd.colors = o3d.utility.Vector3dVector(colors)

    return pcd


def visualize_pcd(*pcds, point_size=10.0):
    # 创建一个可视化窗口
    vis = o3d.visualization.Visualizer()
    vis.create_window()

    # 将所有点云添加到视图
    for pcd in pcds:
        vis.add_geometry(pcd)

    # 设置点的大小
    render_option = vis.get_render_option()
    render_option.point_size = point_size

    # 运行可视化
    vis.run()
    vis.destroy_window()


def get_rotation_matrix(axis, angle):
    """返回绕指定轴旋转angle弧度的旋转矩阵"""
    if axis == 'x':
        return np.array([
            [1, 0, 0],
            [0, np.cos(angle), -np.sin(angle)],
            [0, np.sin(angle), np.cos(angle)]
        ])
    elif axis == 'y':
        return np.array([
            [np.cos(angle), 0, np.sin(angle)],
            [0, 1, 0],
            [-np.sin(angle), 0, np.cos(angle)]
        ])
    elif axis == 'z':
        return np.array([
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1]
        ])
    else:
        raise ValueError("Axis must be one of 'x', 'y', or 'z'")