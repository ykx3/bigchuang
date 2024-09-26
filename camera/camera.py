import json
import os
import re
import time
import subprocess
from .utils import read_color_image, read_depth_image, rgbd2cloud


class RGBDCamera:
    """
    奥比中光相机

    注：应该是单例对象
    """

    def __init__(self):
        """
        初始化 RGBDCamera 实例。
        """
        self.image_path = os.path.join(os.path.realpath(__file__)[:-10], 'image_cache')
        if not os.path.exists(self.image_path):
            os.mkdir(self.image_path)
        os.chdir(self.image_path)
        try:
            result = subprocess.run(['../csource/ParamentsGet'], capture_output=True, text=True, check=True)

            def extract_params_from_string(s):
                # 定义正则表达式模式来匹配 "paraments:" 后面的 JSON 字符串
                pattern = re.compile(r'Parameters:\s*(\{.*?\})', re.DOTALL)

                # 在字符串中搜索匹配项
                match = pattern.search(s)

                if match:
                    # 提取匹配到的 JSON 字符串
                    params_json = match.group(1)

                    try:
                        # 尝试将 JSON 字符串转换成 Python 字典
                        params_dict = json.loads(params_json)
                        return params_dict
                    except json.JSONDecodeError:
                        print("无法解析参数字典，可能不是有效的 JSON 格式")
                        return None
                else:
                    print("未找到 'Parameters:' 关键字")
                    return None
            self.paraments = extract_params_from_string(result.stdout)
            # print(self.paraments)
        except subprocess.CalledProcessError as e:
            print(f"错误: 子进程返回非零退出状态 {e.returncode}")
            print("标准输出:")
            print(e.stdout)
            print("标准错误:")
            print(e.stderr)

        except Exception as e:
            print(f"错误: {e}")

    def get_frame(self):
        """
        获取最新的彩色图像和深度图像对。

        Returns:
            tuple: 包含彩色图像和深度图像的元组。如果找不到匹配的图像对，则返回 (None, None)。
        """
        subprocess.run(['../csource/RGBDSaver'], stdout=subprocess.DEVNULL, )
        color_path = f'{self.image_path}/Color_0.png'
        depth_path = f'{self.image_path}/Depth_0.png'
        color_image = read_color_image(color_path)
        depth_image = read_depth_image(depth_path)
        os.remove(color_path)
        os.remove(depth_path)
        return color_image, depth_image

    def get_depth(self):
        """
        获取最新的深度图像。

        Returns:
            numpy.ndarray or None: 深度图像。如果找不到深度图像，则返回 None。
        """
        return self.get_frame()[0]

    def get_color(self):
        """
        获取最新的彩色图像。

        Returns:
            numpy.ndarray or None: 彩色图像。如果找不到彩色图像，则返回 None。
        """
        return self.get_frame()[1]

    def get_para(self):
        return self.paraments

    def get_pcd(self):
        color, depth = self.get_frame()
        para = self.get_para()
        pcd = rgbd2cloud(color_image=color, depth_image=depth, **para, depth_scale=1)
        return pcd