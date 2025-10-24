# PyInstaller hook for OpenCV
# 确保OpenCV的所有必要文件都被包含

from PyInstaller.utils.hooks import collect_data_files, collect_submodules
import cv2
import os

# 收集OpenCV的所有子模块
hiddenimports = collect_submodules('cv2')

# 收集OpenCV的数据文件
datas = collect_data_files('cv2')

# 添加OpenCV的配置文件
cv2_path = os.path.dirname(cv2.__file__)
config_files = []
for root, dirs, files in os.walk(cv2_path):
    for file in files:
        if file.endswith('.py') and 'config' in file.lower():
            config_files.append(os.path.join(root, file))

# 确保包含所有必要的OpenCV文件
hiddenimports.extend([
    'cv2.config',
    'cv2.loader',
    'cv2.utils',
    'cv2.data',
])

print(f"OpenCV hook: Found {len(hiddenimports)} hidden imports")
print(f"OpenCV hook: Found {len(datas)} data files")
print(f"OpenCV hook: Found {len(config_files)} config files")