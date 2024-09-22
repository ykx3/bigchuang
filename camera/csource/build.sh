#!/bin/bash

# 检查是否提供了SDKPath参数
if [ -z "$1" ]; then
  echo "Usage: $0 <SDKPath>"
  exit 1
fi

# 获取SDKPath参数
SDKPath="$1"

# 检查SDKPath是否存在
if [ ! -d "$SDKPath" ]; then
  echo "Error: SDKPath directory does not exist: $SDKPath"
  exit 1
fi

# 创建构建目录
BUILD_DIR="build"
rm -rf $BUILD_DIR
mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"

# 运行CMake配置
cmake .. -DOrbbecSDK_ROOT_DIR="$SDKPath" || {
  echo "Error: CMake configuration failed."
  exit 1
}

# 编译项目
make -j$(nproc) || {
  echo "Error: Build failed."
  exit 1
}

cp bin/RGBDSaver ..
echo "Build completed successfully."

# 可选：运行生成的可执行文件
# ./RGBDSaver