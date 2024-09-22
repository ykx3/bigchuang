import time
import matplotlib.pyplot as plt
from camera import RGBDCamera
camera = RGBDCamera(fps=10)
color, depth = camera.get_frame()
if color is not None:
    plt.imshow(color)
    plt.show()
if depth is not None:
    plt.imshow(depth)
    plt.show()
# cnt = 0
# for i in range(10):
#     time.sleep(0.1)
#     a, b = camera.get_frame()
#     cnt += a is None or b is None
# print(cnt)