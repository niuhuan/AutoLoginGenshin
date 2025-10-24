"""
PyInstaller hook for pywin32
确保pywin32相关模块被正确包含
"""
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# 收集所有pywin32子模块
hiddenimports = collect_submodules('win32gui')
hiddenimports.extend(collect_submodules('win32api'))
hiddenimports.extend(collect_submodules('win32con'))
hiddenimports.extend(collect_submodules('win32process'))
hiddenimports.extend(collect_submodules('pywin32'))

# 收集数据文件
datas = collect_data_files('pywin32')

print(f"PyWin32 hook: Found {len(hiddenimports)} hidden imports")
print(f"PyWin32 hook: Found {len(datas)} data files")
