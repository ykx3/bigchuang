### RGBDCamera 类 - 文档

#### 概述
`RGBDCamera` 类用于管理与奥比中光（Orbbec）RGBD 相机相关的操作，包括图像的捕获与处理。该类设计为单例模式，意味着在整个程序生命周期中只存在一个 `RGBDCamera` 实例。它通过启动一个外部 C++ 程序来获取 RGB 图像和深度图，并将这些数据存储在指定的缓存目录中。`RGBDCamera` 提供了方法来读取这些缓存中的图像文件，并返回相应的图像数据。

#### 属性
- **image_path**: 存储图像缓存的路径，默认是在当前模块所在目录下创建名为 `image_cache` 的文件夹。
- **process**: 启动的外部 C++ 程序的 `subprocess.Popen` 对象，用于控制 RGBD 图像的捕获。

#### 构造函数
- **__init__()**: 初始化 `RGBDCamera` 实例。

#### 方法
- **get_frame()**: 获取最新的彩色图像和深度图像对。如果找不到匹配的图像对，则返回 `(None, None)`。
- **get_depth()**: 获取最新的深度图像。如果找不到深度图像，则返回 `None`。
- **get_color()**: 获取最新的彩色图像。如果找不到彩色图像，则返回 `None`。

#### 析构函数
- **__del__()**: 当 `RGBDCamera` 实例被销毁时，终止与之关联的外部 C++ 程序，并确保所有相关资源被正确释放。

#### 使用示例
```python
from camera import *

camera = RGBDCamera()

# 获取一帧图像
color_image, depth_image = camera.get_frame()
if color_image is not None and depth_image is not None:
    # 处理图像数据...
    pass

# 清理
del camera
```

#### 注意事项
- 在使用 `RGBDCamera` 之前，请确保已经安装并配置好了所需的外部 C++ 程序 `RGBDSaver`。
- 由于该类使用了 `subprocess` 模块来启动外部程序，因此需要注意程序的安全性和稳定性。
- 如果需要从多线程或多进程中访问 `RGBDCamera` 实例，建议采取适当的同步机制以避免竞态条件。
- `RGBDCamera` 实例应该谨慎地创建和销毁，尤其是在长时间运行的应用程序中，以防止资源泄漏。

#### 依赖项
- `subprocess`: 用于启动和管理外部程序。
- `os`: 用于文件和目录操作。
- `utils.read_color_image`, `utils.read_depth_image`: 自定义的辅助函数，用于读取和解析图像文件。

#### 兼容性
此代码示例假设操作系统为 Linux 或 macOS，因为 Windows 上的路径处理和子进程管理可能有所不同。如果需要在 Windows 上使用，可能需要调整路径处理逻辑和子进程调用方式。

注：此文档由文心一言生成

### 安装
```bash
cd camera/csource
./build.sh /path/to/sdk
```