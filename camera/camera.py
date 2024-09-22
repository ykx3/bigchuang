import os
import time
import subprocess
from .utils import read_color_image, read_depth_image


class RGBDCamera:
    """
    奥比中光相机

    注：应该是单例对象
    """

    def __init__(self, fps=10.0):
        """
        初始化 RGBDCamera 实例，设置图像捕获的帧率。

        Args:
            fps (float): 每秒捕获的帧数，默认值为 10.0 帧/秒。
        """
        self.image_path = os.path.join(os.path.realpath(__file__)[:-10], 'image_cache')
        if not os.path.exists(self.image_path):
            os.mkdir(self.image_path)
        os.chdir(self.image_path)
        # print('分配rgbd资源初始化rgbd相机')
        self.process = subprocess.Popen(['../csource/RGBDSaver', str(1 / fps)], stdout=subprocess.DEVNULL, )
        time.sleep(1)

    def get_frame(self):
        """
        获取最新的彩色图像和深度图像对。

        Returns:
            tuple: 包含彩色图像和深度图像的元组。如果找不到匹配的图像对，则返回 (None, None)。
        """
        f = True
        color_image, depth_image = None, None
        for i in range(5):
            color_path = f'{self.image_path}/Color_{i}.png'
            depth_path = f'{self.image_path}/Depth_{i}.png'
            if f and os.path.exists(depth_path) and os.path.exists(color_path):
                color_image = read_color_image(color_path)
                depth_image = read_depth_image(depth_path)
                f = False
            # if os.path.exists(color_path):
            #     os.remove(color_path)
            # if os.path.exists(depth_path):
            #     os.remove(depth_path)
        return color_image, depth_image

    def get_depth(self):
        """
        获取最新的深度图像。

        Returns:
            numpy.ndarray or None: 深度图像。如果找不到深度图像，则返回 None。
        """
        f = True
        depth_image = None
        for i in range(5):
            depth_path = f'{self.image_path}/Depth_{i}.png'
            if f and os.path.exists(depth_path):
                depth_image = read_depth_image(depth_path)
            if os.path.exists(depth_path):
                os.remove(depth_path)
        return depth_image

    def get_color(self):
        """
        获取最新的彩色图像。

        Returns:
            numpy.ndarray or None: 彩色图像。如果找不到彩色图像，则返回 None。
        """
        f = True
        color_image = None
        for i in range(5):
            color_path = f'{self.image_path}/Color_{i}.png'
            if f and os.path.exists(color_path):
                color_image = read_color_image(color_path)
                f = False
            if os.path.exists(color_path):
                os.remove(color_path)
        return color_image

    def __del__(self):
        """
        当 RGBDCamera 实例被销毁时，终止与之关联的外部 C++ 程序，并确保所有相关资源被正确释放。
        """
        if self.process:
            # 终止子进程
            self.process.terminate()

            # 等待子进程资源被回收
            self.process.wait()
            # print("资源已回收")
