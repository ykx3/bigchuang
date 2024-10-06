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


def remove_outliers(pcd, nb_neighbors=20, std_ratio=2.0):
    # 使用统计学方法去除离群点
    cl, ind = pcd.remove_statistical_outlier(nb_neighbors=nb_neighbors, std_ratio=std_ratio)
    return pcd.select_by_index(ind)


def get_largest_cluster(pcd):
    # 使用 DBSCAN 进行聚类
    with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Error) as cm:
        labels = np.array(pcd.cluster_dbscan(eps=0.04, min_points=20, print_progress=False))

    # 计算每个类的点数
    unique_labels, counts = np.unique(labels, return_counts=True)

    # 移除背景的标签（如果存在），一般为-1
    mask = unique_labels != -1
    unique_labels = unique_labels[mask]
    counts = counts[mask]

    # 只有一个有效簇的情况，无第二大簇
    if unique_labels.size < 2:
        if unique_labels.size == 0:
            return pcd, None
        largest_cluster_pcd = pcd.select_by_index(np.where(labels == unique_labels[0])[0])
        return remove_outliers(largest_cluster_pcd), None

    # 找出第一和第二大簇的标签
    sorted_indices = np.argsort(-counts)  # 对点数进行降序排序并返回索引
    largest_label = unique_labels[sorted_indices[0]]
    second_largest_label = unique_labels[sorted_indices[1]]

    # 获取第一大簇的点云
    largest_cluster_indices = np.where(labels == largest_label)[0]
    largest_cluster_pcd = pcd.select_by_index(largest_cluster_indices)
    largest_cluster_pcd = remove_outliers(largest_cluster_pcd)

    # 获取第二大簇的点云
    second_largest_cluster_indices = np.where(labels == second_largest_label)[0]
    second_largest_cluster_pcd = pcd.select_by_index(second_largest_cluster_indices)
    second_largest_cluster_pcd = remove_outliers(second_largest_cluster_pcd)
    if len(largest_cluster_pcd.points) * 0.5 > len(second_largest_cluster_pcd.points):
        return largest_cluster_pcd, None
    return largest_cluster_pcd, second_largest_cluster_pcd
