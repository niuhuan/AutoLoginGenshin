"""
管理员权限检查和获取模块
"""
import sys
import os
import ctypes
import subprocess


def is_admin():
    """检查当前是否具有管理员权限"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    """以管理员权限重新运行程序"""
    if is_admin():
        return True
    else:
        # 重新以管理员权限启动
        try:
            # 判断是exe文件还是python脚本
            if sys.argv[0].endswith('.exe'):
                # exe文件：排除程序路径，只传递实际参数
                args = sys.argv[1:] if len(sys.argv) > 1 else []
                args_str = " ".join(args)
                executable = sys.argv[0]  # 使用exe文件本身
                print(f"[EXE模式] 重新启动参数: {sys.argv}")
                print(f"[EXE模式] 传递参数: {args_str}")
            else:
                # python脚本：保持完整参数（包括脚本路径）
                args_str = " ".join(sys.argv)
                executable = sys.executable
                print(f"[Python模式] 重新启动参数: {sys.argv}")
                print(f"[Python模式] 传递参数: {args_str}")
            
            ctypes.windll.shell32.ShellExecuteW(
                None, 
                "runas", 
                executable, 
                args_str, 
                None, 
                1
            )
            return True
        except Exception as e:
            print(f"获取管理员权限失败: {e}")
            return False


def check_and_request_admin():
    """检查并请求管理员权限"""
    if not is_admin():
        print("检测到需要管理员权限，正在请求权限...")
        if run_as_admin():
            print("已获取管理员权限，程序将重新启动")
            sys.exit(0)
        else:
            print("无法获取管理员权限，程序可能无法正常工作")
            return False
    return True


def switch_to_game_window():
    """切换到游戏窗口"""
    try:
        import win32gui
        import win32con
        import ctypes
        import psutil
        
        def set_foreground_window_with_retry(hwnd):
            """尝试将窗口设置为前台，失败时先最小化再恢复"""
            def toggle_window_state(hwnd, minimize=False):
                """最小化或恢复窗口"""
                SW_MINIMIZE = 6
                SW_RESTORE = 9
                state = SW_MINIMIZE if minimize else SW_RESTORE
                ctypes.windll.user32.ShowWindow(hwnd, state)

            toggle_window_state(hwnd, minimize=False)
            if ctypes.windll.user32.SetForegroundWindow(hwnd) == 0:
                toggle_window_state(hwnd, minimize=True)
                toggle_window_state(hwnd, minimize=False)
                if ctypes.windll.user32.SetForegroundWindow(hwnd) == 0:
                    raise Exception("Failed to set window foreground")
        
        # 尝试多种方式查找游戏窗口
        hwnd = None
        found_method = ""
        
        # 方法1: 通过窗口标题查找
        def enum_windows_callback(hwnd_test, windows):
            if win32gui.IsWindowVisible(hwnd_test):
                window_title = win32gui.GetWindowText(hwnd_test)
                window_class = win32gui.GetClassName(hwnd_test)
                print(f"发现窗口: 标题='{window_title}', 类名='{window_class}', HWND={hwnd_test}")
                if ('原神' in window_title or 'Genshin Impact' in window_title or 
                    'YuanShen' in window_title or 'genshin' in window_title.lower()):
                    windows.append((hwnd_test, window_title, window_class))
            return True
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        
        if windows:
            hwnd, title, class_name = windows[0]
            found_method = f"窗口标题: {title}"
            print(f"✅ 通过窗口标题找到游戏窗口: {title}")
        else:
            print("❌ 通过窗口标题未找到游戏窗口，尝试通过进程查找...")
            
            # 方法2: 通过进程名查找
            yuan_shen_processes = []
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'] and 'YuanShen.exe' in proc.info['name']:
                        yuan_shen_processes.append(proc.info['pid'])
                        print(f"找到YuanShen进程: PID={proc.info['pid']}")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if yuan_shen_processes:
                # 通过进程ID查找窗口
                for pid in yuan_shen_processes:
                    def enum_windows_by_pid(hwnd_test, target_pid):
                        if win32gui.IsWindowVisible(hwnd_test):
                            _, found_pid = win32gui.GetWindowThreadProcessId(hwnd_test)
                            if found_pid == target_pid:
                                window_title = win32gui.GetWindowText(hwnd_test)
                                window_class = win32gui.GetClassName(hwnd_test)
                                print(f"通过进程ID找到窗口: PID={target_pid}, 标题='{window_title}', 类名='{window_class}', HWND={hwnd_test}")
                                return (hwnd_test, window_title, window_class)
                        return None
                    
                    result = win32gui.EnumWindows(enum_windows_by_pid, pid)
                    if result:
                        hwnd, title, class_name = result
                        found_method = f"进程ID: {pid}"
                        break
        
        if hwnd:
            print(f"尝试激活窗口: HWND={hwnd}, 方法={found_method}")
            try:
                set_foreground_window_with_retry(hwnd)
                print("✅ 成功切换到游戏窗口")
                return True
            except Exception as e:
                print(f"❌ 激活窗口失败: {e}")
                # 尝试备用方法
                try:
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    win32gui.SetForegroundWindow(hwnd)
                    print("✅ 使用备用方法成功切换到游戏窗口")
                    return True
                except Exception as e2:
                    print(f"❌ 备用方法也失败: {e2}")
                    return False
        else:
            print("❌ 未找到游戏窗口")
            return False
            
    except ImportError:
        print("❌ 需要安装pywin32库来支持窗口切换功能")
    except Exception as e:
        print(f"❌ 切换窗口失败: {e}")
    return False


def create_manifest():
    """创建应用程序清单文件，请求管理员权限"""
    manifest_content = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity
    version="1.0.0.0"
    processorArchitecture="*"
    name="GenshinAutoLogin"
    type="win32"
  />
  <description>原神自动登录工具</description>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v2">
    <security>
      <requestedPrivileges xmlns="urn:schemas-microsoft-com:asm.v3">
        <requestedExecutionLevel level="requireAdministrator" uiAccess="false"/>
      </requestedPrivileges>
    </security>
  </trustInfo>
</assembly>'''
    
    with open("app.manifest", "w", encoding="utf-8") as f:
        f.write(manifest_content)
    
    return "app.manifest"
