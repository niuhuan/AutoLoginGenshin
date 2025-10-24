"""
原神游戏管理核心逻辑模块
"""
import os
import psutil
import subprocess
import time
from config_manager import ConfigManager
from logger import get_logger
from screen_recognition import ScreenRecognition


class GameManager:
    """游戏管理器类"""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.logger = get_logger()
        self.screen_recognition = ScreenRecognition()
        
        # 初始化屏幕识别模板
        self._init_screen_recognition()
    
    def _init_screen_recognition(self):
        """初始化屏幕识别模板"""
        try:
            # 查找进入游戏按钮模板
            template_path = os.path.join(os.path.dirname(__file__), 'assets', 'enter_game.png')
            if os.path.exists(template_path):
                self.screen_recognition.load_template(template_path)
                self.logger.info("✅ 屏幕识别模板加载成功")
            else:
                self.logger.warning(f"⚠️ 屏幕识别模板不存在: {template_path}")
        except Exception as e:
            self.logger.error(f"初始化屏幕识别失败: {e}")
    
    def get_game_path(self):
        """获取游戏路径"""
        return self.config_manager.get_game_path()
    
    def set_game_path(self, path):
        """设置游戏路径"""
        return self.config_manager.set_game_path(path)
    
    def is_game_running(self):
        """检测原神游戏是否正在运行"""
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] and 'YuanShen.exe' in proc.info['name']:
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False
    
    def switch_to_game_window(self):
        """切换到游戏窗口"""
        try:
            import win32gui
            import win32con
            import ctypes
            import psutil
            
            def set_foreground_window_with_retry(hwnd, logger):
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
                    self.logger.debug(f"发现窗口: 标题='{window_title}', 类名='{window_class}', HWND={hwnd_test}")
                    if ('原神' in window_title or 'Genshin Impact' in window_title or 
                        'YuanShen' in window_title or 'genshin' in window_title.lower()):
                        windows.append((hwnd_test, window_title, window_class))
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            if windows:
                hwnd, title, class_name = windows[0]
                found_method = f"窗口标题: {title}"
                self.logger.info(f"✅ 通过窗口标题找到游戏窗口: {title}")
            else:
                self.logger.warning("❌ 通过窗口标题未找到游戏窗口，尝试通过进程查找...")
                
                # 方法2: 通过进程名查找
                yuan_shen_processes = []
                for proc in psutil.process_iter(['pid', 'name']):
                    try:
                        if proc.info['name'] and 'YuanShen.exe' in proc.info['name']:
                            yuan_shen_processes.append(proc.info['pid'])
                            self.logger.debug(f"找到YuanShen进程: PID={proc.info['pid']}")
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
                                    self.logger.debug(f"通过进程ID找到窗口: PID={target_pid}, 标题='{window_title}', 类名='{window_class}', HWND={hwnd_test}")
                                    return (hwnd_test, window_title, window_class)
                            return None
                        
                        result = win32gui.EnumWindows(enum_windows_by_pid, pid)
                        if result:
                            hwnd, title, class_name = result
                            found_method = f"进程ID: {pid}"
                            break
            
            if hwnd:
                self.logger.debug(f"尝试激活窗口: HWND={hwnd}, 方法={found_method}")
                try:
                    set_foreground_window_with_retry(hwnd, self.logger)
                    self.logger.info("✅ 成功切换到游戏窗口")
                    return True
                except Exception as e:
                    self.logger.warning(f"❌ 激活窗口失败: {e}")
                    # 尝试备用方法
                    try:
                        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                        win32gui.SetForegroundWindow(hwnd)
                        self.logger.info("✅ 使用备用方法成功切换到游戏窗口")
                        return True
                    except Exception as e2:
                        self.logger.error(f"❌ 备用方法也失败: {e2}")
                        return False
            else:
                self.logger.warning("❌ 未找到游戏窗口")
                return False
                
        except ImportError:
            self.logger.warning("❌ 需要安装pywin32库来支持窗口切换功能")
        except Exception as e:
            self.logger.error(f"❌ 切换窗口失败: {e}")
        return False
    
    def launch_game(self, game_path=None):
        """启动游戏"""
        if game_path is None:
            game_path = self.get_game_path()
        
        if not game_path:
            self.logger.error("错误: 未设置游戏路径")
            return False
        
        if not os.path.exists(game_path):
            self.logger.error(f"错误: 游戏文件不存在: {game_path}")
            return False
        
        try:
            subprocess.Popen([game_path], cwd=os.path.dirname(game_path))
            self.logger.info("游戏启动成功")
            return True
        except Exception as e:
            self.logger.error(f"启动游戏失败: {e}")
            return False
    
    def handle_login(self, username=None, password=None, game_path=None):
        """统一的登录处理方法，支持GUI和命令行"""
        try:
            # 检查游戏是否已在运行
            if self.is_game_running():
                self.logger.info("原神游戏已在运行，正在切换到游戏窗口...")
                success = self.switch_to_game_window()
                if success:
                    self.logger.info("✅ 已成功切换到游戏窗口！")
                    
                    # 切换窗口后等待30秒
                    self.logger.info("等待30秒让游戏完全加载...")
                    time.sleep(30)
                    
                    # 检测是否需要登录
                    self._check_and_handle_login(username, password)
                    return True
                else:
                    self.logger.warning("❌ 无法切换到游戏窗口，请手动切换")
                    return False
            else:
                # 游戏未运行，需要启动游戏
                # 使用提供的路径或默认路径
                if game_path:
                    self.set_game_path(game_path)
                
                current_path = self.get_game_path()
                if not current_path:
                    self.logger.error("错误: 未找到游戏路径配置")
                    return False
                
                # 验证游戏路径
                is_valid, message = self.validate_game_path(current_path)
                if not is_valid:
                    self.logger.error(f"游戏路径无效: {message}")
                    return False
                
                # 启动游戏
                if username:
                    self.logger.info(f"将使用账号 {username} 启动原神游戏...")
                else:
                    self.logger.info("启动原神游戏...")
                
                success = self.launch_game(current_path)
                if success:
                    self.logger.info("✅ 游戏启动成功！")
                    
                    # 游戏启动后等待60秒
                    self.logger.info("等待60秒让游戏完全加载...")
                    time.sleep(60)
                    
                    # 检测是否需要登录
                    self._check_and_handle_login(username, password)
                    return True
                else:
                    self.logger.error("❌ 游戏启动失败")
                    return False
                    
        except Exception as e:
            self.logger.error(f"登录处理失败: {e}")
            return False
    
    def _check_and_handle_login(self, username=None, password=None):
        """检测并处理登录（带重试机制）"""
        max_retries = 2  # 最多重试2次
        retry_interval = 30  # 重试间隔30秒
        
        for attempt in range(max_retries + 1):  # 0, 1, 2 共3次尝试
            try:
                if attempt > 0:
                    self.logger.info(f"🔄 第 {attempt + 1} 次尝试检测登录窗口...")
                else:
                    self.logger.info("开始检测屏幕内容...")
                
                # 检测是否存在进入游戏按钮
                if self._detect_enter_game_button():
                    self.logger.info("🔍 检测到进入游戏按钮，需要登录")
                    
                    if username and password:
                        self.logger.info(f"开始自动登录流程，用户名: {username}")
                        login_success = self._perform_auto_login(username, password)
                        
                        if login_success:
                            self.logger.info("🎉 自动登录完成！程序将在3秒后退出...")
                            time.sleep(3)
                            self.logger.info("程序退出")
                            import sys
                            sys.exit(0)
                        else:
                            self.logger.error("❌ 自动登录失败")
                            return  # 登录失败直接返回，不重试
                    else:
                        self.logger.warning("⚠️ 检测到需要登录，但未提供用户名和密码")
                        self.logger.info("请手动登录或使用 -u 和 -p 参数提供账号信息")
                        return  # 没有账号密码直接返回
                else:
                    if attempt < max_retries:
                        self.logger.info(f"❌ 第 {attempt + 1} 次检测未发现登录窗口")
                        self.logger.info(f"⏰ 等待 {retry_interval} 秒后进行第 {attempt + 2} 次检测...")
                        time.sleep(retry_interval)
                    else:
                        self.logger.info("✅ 经过多次检测，确认无需登录")
                        return
                    
            except Exception as e:
                self.logger.error(f"第 {attempt + 1} 次检测登录状态失败: {e}")
                if attempt < max_retries:
                    self.logger.info(f"⏰ 等待 {retry_interval} 秒后重试...")
                    time.sleep(retry_interval)
                else:
                    self.logger.error("❌ 所有检测尝试均失败")
                    return
    
    def _detect_enter_game_button(self, threshold=0.8):
        """检测屏幕中是否存在进入游戏按钮"""
        try:
            self.logger.info("开始检测进入游戏按钮...")
            
            # 截取屏幕
            screenshot = self._capture_screen()
            if screenshot is None:
                return False
            
            # 查找模板
            top_left, bottom_right = self._find_template_in_screen(screenshot, threshold)
            
            if top_left is not None and bottom_right is not None:
                self.logger.info("✅ 检测到进入游戏按钮，需要登录")
                return True
            else:
                self.logger.info("❌ 未检测到进入游戏按钮，无需登录")
                return False
                
        except Exception as e:
            self.logger.error(f"检测进入游戏按钮失败: {e}")
            return False
    
    def _capture_screen(self):
        """截取屏幕"""
        try:
            import pyautogui
            import numpy as np
            import cv2
            
            # 使用pyautogui截取屏幕
            screenshot = pyautogui.screenshot()
            # 转换为OpenCV格式
            screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            return screenshot_cv
        except Exception as e:
            self.logger.error(f"截取屏幕失败: {e}")
            return None
    
    def find_template_in_image(self, target_image, template_image, threshold=0.8):
        """在目标图片中查找模板图片（抽象方法）"""
        try:
            import cv2
            
            if target_image is None:
                self.logger.error("目标图片为空")
                return None, None, 0.0
                
            if template_image is None:
                self.logger.error("模板图片为空")
                return None, None, 0.0
            
            # 使用模板匹配
            result = cv2.matchTemplate(target_image, template_image, cv2.TM_CCOEFF_NORMED)
            
            # 查找匹配位置
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            self.logger.debug(f"模板匹配结果: 最大相似度={max_val:.3f}, 阈值={threshold}")
            
            if max_val >= threshold:
                # 计算匹配区域
                h, w = template_image.shape[:2]
                top_left = max_loc
                bottom_right = (top_left[0] + w, top_left[1] + h)
                
                self.logger.info(f"找到匹配区域: 相似度={max_val:.3f}, 位置={top_left}, 尺寸={w}x{h}")
                return top_left, bottom_right, max_val
            else:
                self.logger.debug(f"未找到匹配区域: 相似度={max_val:.3f} < 阈值={threshold}")
                return None, None, max_val
                
        except Exception as e:
            self.logger.error(f"模板匹配失败: {e}")
            return None, None, 0.0
    
    def _find_template_in_screen(self, screenshot=None, threshold=0.8):
        """在屏幕中查找模板图片（保持向后兼容）"""
        try:
            if screenshot is None:
                screenshot = self._capture_screen()
                
            if screenshot is None:
                return None, None
                
            if self.screen_recognition.enter_game_template is None:
                self.logger.error("模板图片未加载")
                return None, None
            
            # 使用抽象的模板匹配方法
            top_left, bottom_right, similarity = self.find_template_in_image(
                screenshot, 
                self.screen_recognition.enter_game_template, 
                threshold
            )
            
            if top_left is not None and bottom_right is not None:
                return top_left, bottom_right
            else:
                return None, None
                
        except Exception as e:
            self.logger.error(f"屏幕模板匹配失败: {e}")
            return None, None
    
    def _perform_auto_login(self, username, password):
        """执行自动登录"""
        try:
            self.logger.info("开始执行自动登录...")
            
            # 等待一下让界面稳定
            time.sleep(2)
            
            # 1. 检测并点击圆圈（如果存在）
            if self._detect_and_click_circle():
                time.sleep(1)
            
            # 2. 点击进入游戏按钮（如果存在）
            if self._click_enter_game_button():
                time.sleep(1)
            
            # 3. 查找并点击账号输入框
            if self._click_account_field():
                time.sleep(0.5)
                # 清空输入框并输入账号
                self._secretly_write(username)
                time.sleep(0.5)
            
            # 4. 查找并点击密码输入框
            if self._click_password_field():
                time.sleep(0.5)
                # 清空输入框并输入密码
                self._secretly_write(password)
                time.sleep(0.5)
            
            # 5. 点击登录按钮
            if self._click_login_button():
                self.logger.info("✅ 登录信息输入完成，等待登录处理...")
                time.sleep(3)  # 等待登录处理
                
                # 6. 再次点击进入游戏按钮（登录后可能需要再次点击）
                if self._click_enter_game_button():
                    self.logger.info("✅ 已点击进入游戏按钮，登录流程完成")
                    time.sleep(2)  # 等待游戏启动
                    return True
                else:
                    self.logger.warning("⚠️ 未找到进入游戏按钮，但登录信息已输入")
                    return True
            else:
                self.logger.warning("❌ 未找到登录按钮")
                return False
                
        except Exception as e:
            self.logger.error(f"自动登录失败: {e}")
            return False
    
    def _ensure_IME_lang_en(self):
        """切换输入法语言/键盘语言至英文"""
        try:
            import win32api
            import win32gui
            from win32con import WM_INPUTLANGCHANGEREQUEST
            
            EN = 0x0409
            hwnd = win32gui.GetForegroundWindow()
            result = win32api.SendMessage(hwnd, WM_INPUTLANGCHANGEREQUEST, 0, EN)
            
            if result == 0:
                self.logger.debug("✅ 输入法已切换至英文")
                return True
            else:
                self.logger.warning("⚠️ 输入法切换失败")
                return False
                
        except Exception as e:
            self.logger.error(f"切换输入法失败: {e}")
            return False
    
    def _secretly_write(self, text, interval=0.1):
        """模拟键盘输入字符串（不输出具体内容到日志）"""
        try:
            import pyautogui
            
            # 确保输入法为英文
            self._ensure_IME_lang_en()
            
            # 模拟键盘输入
            pyautogui.write(text, interval=interval)
            self.logger.debug(f"已输入账号密码（长度: {len(text)}）")
            return True
            
        except Exception as e:
            self.logger.error(f"键盘输入失败: {e}")
            return False
    
    def _click_enter_game_button(self, threshold=0.8):
        """点击进入游戏按钮"""
        try:
            import pyautogui
            
            self.logger.info("尝试点击进入游戏按钮...")
            
            # 查找按钮位置
            top_left, bottom_right = self._find_template_in_screen(threshold=threshold)
            
            if top_left is not None and bottom_right is not None:
                # 计算按钮中心点
                center_x = (top_left[0] + bottom_right[0]) // 2
                center_y = (top_left[1] + bottom_right[1]) // 2
                
                self.logger.info(f"点击按钮中心位置: ({center_x}, {center_y})")
                
                # 点击按钮
                pyautogui.click(center_x, center_y)
                self.logger.info("✅ 已点击进入游戏按钮")
                return True
            else:
                self.logger.warning("❌ 未找到进入游戏按钮，无法点击")
                return False
                
        except Exception as e:
            self.logger.error(f"点击进入游戏按钮失败: {e}")
            return False
    
    def handle_game_launch(self):
        """处理游戏启动逻辑（保持向后兼容）"""
        return self.handle_login()
    
    def validate_game_path(self, path):
        """验证游戏路径是否有效"""
        return self.config_manager.validate_game_path(path)
    
    def _click_account_field(self):
        """点击账号输入框"""
        try:
            import pyautogui
            import cv2
            
            self.logger.info("尝试点击账号输入框...")
            
            # 加载账号输入框模板
            username_template_path = os.path.join(os.path.dirname(__file__), 'assets', 'input_username.png')
            if not os.path.exists(username_template_path):
                self.logger.warning(f"账号输入框模板不存在: {username_template_path}")
                return False
            
            username_template = cv2.imread(username_template_path, cv2.IMREAD_COLOR)
            if username_template is None:
                self.logger.error("无法加载账号输入框模板")
                return False
            
            # 截取屏幕
            screenshot = self._capture_screen()
            if screenshot is None:
                self.logger.error("无法截取屏幕")
                return False
            
            # 使用模板匹配查找账号输入框
            top_left, bottom_right, similarity = self.find_template_in_image(
                screenshot, username_template, threshold=0.7
            )
            
            if top_left is not None and bottom_right is not None:
                # 计算输入框中心点
                center_x = (top_left[0] + bottom_right[0]) // 2
                center_y = (top_left[1] + bottom_right[1]) // 2
                
                self.logger.info(f"✅ 找到账号输入框！位置: ({center_x}, {center_y}), 相似度: {similarity:.3f}")
                
                # 点击输入框
                pyautogui.click(center_x, center_y)
                self.logger.info(f"✅ 已点击账号输入框: ({center_x}, {center_y})")
                return True
            else:
                self.logger.debug(f"未找到账号输入框，最大相似度: {similarity:.3f}")
                return False
                
        except Exception as e:
            self.logger.error(f"点击账号输入框失败: {e}")
            return False
    
    def _click_password_field(self):
        """点击密码输入框"""
        try:
            import pyautogui
            import cv2
            
            self.logger.info("尝试点击密码输入框...")
            
            # 加载密码输入框模板
            password_template_path = os.path.join(os.path.dirname(__file__), 'assets', 'input_password.png')
            if not os.path.exists(password_template_path):
                self.logger.warning(f"密码输入框模板不存在: {password_template_path}")
                return False
            
            password_template = cv2.imread(password_template_path, cv2.IMREAD_COLOR)
            if password_template is None:
                self.logger.error("无法加载密码输入框模板")
                return False
            
            # 截取屏幕
            screenshot = self._capture_screen()
            if screenshot is None:
                self.logger.error("无法截取屏幕")
                return False
            
            # 使用模板匹配查找密码输入框
            top_left, bottom_right, similarity = self.find_template_in_image(
                screenshot, password_template, threshold=0.7
            )
            
            if top_left is not None and bottom_right is not None:
                # 计算输入框中心点
                center_x = (top_left[0] + bottom_right[0]) // 2
                center_y = (top_left[1] + bottom_right[1]) // 2
                
                self.logger.info(f"✅ 找到密码输入框！位置: ({center_x}, {center_y}), 相似度: {similarity:.3f}")
                
                # 点击输入框
                pyautogui.click(center_x, center_y)
                self.logger.info(f"✅ 已点击密码输入框: ({center_x}, {center_y})")
                return True
            else:
                self.logger.debug(f"未找到密码输入框，最大相似度: {similarity:.3f}")
                return False
                
        except Exception as e:
            self.logger.error(f"点击密码输入框失败: {e}")
            return False
    
    def _click_login_button(self):
        """点击登录按钮"""
        try:
            import pyautogui
            
            self.logger.info("尝试点击登录按钮...")
            
            # 这里应该使用模板匹配找到登录按钮的位置
            # 暂时使用固定坐标（需要根据实际游戏界面调整）
            login_button_x = 960  # 屏幕中心
            login_button_y = 500  # 大概的登录按钮位置
            
            pyautogui.click(login_button_x, login_button_y)
            self.logger.info(f"✅ 已点击登录按钮: ({login_button_x}, {login_button_y})")
            return True
            
        except Exception as e:
            self.logger.error(f"点击登录按钮失败: {e}")
            return False
            
    def _detect_and_click_circle(self):
        """检测并点击圆圈"""
        try:
            import pyautogui
            import cv2
            import numpy as np
            
            self.logger.info("检测圆圈...")
            
            # 加载圆圈模板
            circle_template_path = os.path.join(os.path.dirname(__file__), 'assets', 'circle.png')
            if not os.path.exists(circle_template_path):
                self.logger.warning(f"圆圈模板不存在: {circle_template_path}")
                return False
            
            circle_template = cv2.imread(circle_template_path, cv2.IMREAD_COLOR)
            if circle_template is None:
                self.logger.error("无法加载圆圈模板")
                return False
            
            # 截取屏幕
            screenshot = self._capture_screen()
            if screenshot is None:
                self.logger.error("无法截取屏幕")
                return False
            
            # 使用模板匹配查找圆圈
            top_left, bottom_right, similarity = self.find_template_in_image(
                screenshot, circle_template, threshold=0.7
            )
            
            if top_left is not None and bottom_right is not None:
                # 计算圆圈中心点
                center_x = (top_left[0] + bottom_right[0]) // 2
                center_y = (top_left[1] + bottom_right[1]) // 2
                
                self.logger.info(f"✅ 找到圆圈！位置: ({center_x}, {center_y}), 相似度: {similarity:.3f}")
                
                # 点击圆圈
                pyautogui.click(center_x, center_y)
                self.logger.info(f"✅ 已点击圆圈: ({center_x}, {center_y})")
                return True
            else:
                self.logger.debug(f"未找到圆圈，最大相似度: {similarity:.3f}")
                return False
                
        except Exception as e:
            self.logger.error(f"检测和点击圆圈失败: {e}")
            return False
