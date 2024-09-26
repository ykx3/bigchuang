import time
import matplotlib.pyplot as plt
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
visualize_pcd(pcd)