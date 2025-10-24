"""
测试自动登录功能
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logger import get_logger
from game_manager import GameManager


def test_auto_login():
    """测试自动登录功能"""
    logger = get_logger()
    logger.info("=== 测试自动登录功能 ===")
    
    try:
        # 创建游戏管理器实例
        game_manager = GameManager()
        
        # 测试输入法切换
        logger.info("测试输入法切换...")
        result = game_manager._ensure_IME_lang_en()
        logger.info(f"输入法切换结果: {result}")
        
        # 测试键盘输入（使用测试数据）
        logger.info("测试键盘输入...")
        test_text = "test_username"
        result = game_manager._secretly_write(test_text)
        logger.info(f"键盘输入结果: {result}")
        
        # 测试自动登录流程（使用测试数据）
        logger.info("测试自动登录流程...")
        test_username = "test_user"
        test_password = "test_pass"
        
        # 注意：这里不会真正执行点击操作，只是测试方法调用
        logger.info("注意：以下测试不会真正执行点击操作")
        logger.info("测试账号输入框点击...")
        result1 = game_manager._click_account_field()
        logger.info(f"账号输入框点击结果: {result1}")
        
        logger.info("测试密码输入框点击...")
        result2 = game_manager._click_password_field()
        logger.info(f"密码输入框点击结果: {result2}")
        
        logger.info("测试登录按钮点击...")
        result3 = game_manager._click_login_button()
        logger.info(f"登录按钮点击结果: {result3}")
        
        logger.info("✅ 自动登录功能测试完成")
        logger.info("所有方法都可以正常调用")
        
        return True
        
    except Exception as e:
        logger.critical(f"自动登录功能测试失败: {e}")
        print(f"自动登录功能测试失败: {e}")
        return False


if __name__ == "__main__":
    test_auto_login()
