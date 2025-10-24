"""
屏幕识别和自动登录模块
"""
import time
import cv2
import numpy as np
import pyautogui
from PIL import Image
import os
from logger import get_logger


class ScreenRecognition:
    """屏幕识别类"""
    
    def __init__(self):
        self.logger = get_logger()
        self.enter_game_template = None
        self.template_path = None
        
    def load_template(self, template_path):
        """加载模板图片"""
        try:
            if not os.path.exists(template_path):
                self.logger.error(f"模板图片不存在: {template_path}")
                return False
                
            self.template_path = template_path
            self.enter_game_template = cv2.imread(template_path, cv2.IMREAD_COLOR)
            
            if self.enter_game_template is None:
                self.logger.error(f"无法加载模板图片: {template_path}")
                return False
                
            self.logger.info(f"成功加载模板图片: {template_path}")
            self.logger.info(f"模板图片尺寸: {self.enter_game_template.shape}")
            return True
            
        except Exception as e:
            self.logger.error(f"加载模板图片失败: {e}")
            return False
    
    def capture_screen(self):
        """截取屏幕"""
        try:
            # 使用pyautogui截取屏幕
            screenshot = pyautogui.screenshot()
            # 转换为OpenCV格式
            screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            return screenshot_cv
        except Exception as e:
            self.logger.error(f"截取屏幕失败: {e}")
            return None
    
    def find_template_in_screen(self, screenshot=None, threshold=0.8):
        """在屏幕中查找模板图片"""
        try:
            if screenshot is None:
                screenshot = self.capture_screen()
                
            if screenshot is None:
                return None, None
                
            if self.enter_game_template is None:
                self.logger.error("模板图片未加载")
                return None, None
            
            # 使用模板匹配
            result = cv2.matchTemplate(screenshot, self.enter_game_template, cv2.TM_CCOEFF_NORMED)
            
            # 查找匹配位置
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            self.logger.debug(f"模板匹配结果: 最大相似度={max_val:.3f}, 阈值={threshold}")
            
            if max_val >= threshold:
                # 计算匹配区域
                h, w = self.enter_game_template.shape[:2]
                top_left = max_loc
                bottom_right = (top_left[0] + w, top_left[1] + h)
                
                self.logger.info(f"找到匹配区域: 相似度={max_val:.3f}, 位置={top_left}, 尺寸={w}x{h}")
                return top_left, bottom_right
            else:
                self.logger.debug(f"未找到匹配区域: 相似度={max_val:.3f} < 阈值={threshold}")
                return None, None
                
        except Exception as e:
            self.logger.error(f"模板匹配失败: {e}")
            return None, None
    
    def detect_enter_game_button(self, threshold=0.8):
        """检测屏幕中是否存在进入游戏按钮"""
        try:
            self.logger.info("开始检测进入游戏按钮...")
            
            # 截取屏幕
            screenshot = self.capture_screen()
            if screenshot is None:
                return False
            
            # 查找模板
            top_left, bottom_right = self.find_template_in_screen(screenshot, threshold)
            
            if top_left is not None and bottom_right is not None:
                self.logger.info("✅ 检测到进入游戏按钮，需要登录")
                return True
            else:
                self.logger.info("❌ 未检测到进入游戏按钮，无需登录")
                return False
                
        except Exception as e:
            self.logger.error(f"检测进入游戏按钮失败: {e}")
            return False
    
    def click_enter_game_button(self, threshold=0.8):
        """点击进入游戏按钮"""
        try:
            self.logger.info("尝试点击进入游戏按钮...")
            
            # 查找按钮位置
            top_left, bottom_right = self.find_template_in_screen(threshold=threshold)
            
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
    
    def wait_and_detect_login(self, wait_time=30, check_interval=5, threshold=0.8):
        """等待并检测是否需要登录"""
        try:
            self.logger.info(f"等待 {wait_time} 秒后开始检测登录状态...")
            
            # 等待指定时间
            time.sleep(wait_time)
            
            # 定期检测
            for i in range(0, wait_time, check_interval):
                self.logger.info(f"第 {i//check_interval + 1} 次检测登录状态...")
                
                if self.detect_enter_game_button(threshold):
                    self.logger.info("检测到需要登录，执行自动登录流程")
                    return True
                
                if i + check_interval < wait_time:
                    self.logger.info(f"等待 {check_interval} 秒后进行下次检测...")
                    time.sleep(check_interval)
            
            self.logger.info("检测完成，无需登录")
            return False
            
        except Exception as e:
            self.logger.error(f"等待和检测登录状态失败: {e}")
            return False


def create_screen_recognition():
    """创建屏幕识别实例"""
    return ScreenRecognition()
