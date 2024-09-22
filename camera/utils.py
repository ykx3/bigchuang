import cv2
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
