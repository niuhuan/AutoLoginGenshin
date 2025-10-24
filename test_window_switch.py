"""
窗口切换调试脚本
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game_manager import GameManager
from logger import get_logger
from admin_utils import check_and_request_admin

def test_window_switch():
    """测试窗口切换功能"""
    try:
        logger = get_logger()
        logger.info("=== 原神窗口切换调试测试 ===")
        
        # 检查并请求管理员权限
        if not check_and_request_admin():
            logger.error("无法获取管理员权限，程序退出")
            print("无法获取管理员权限，程序退出")
            sys.exit(1)
        
        logger.info("✅ 已获取管理员权限")
        
        game_manager = GameManager()
        
        # 检查游戏是否运行
        if game_manager.is_game_running():
            logger.info("✅ 检测到原神游戏正在运行")
            logger.info("尝试切换到游戏窗口...")
            
            success = game_manager.switch_to_game_window()
            if success:
                logger.info("✅ 窗口切换成功！")
            else:
                logger.error("❌ 窗口切换失败")
        else:
            logger.warning("❌ 未检测到原神游戏运行")
            logger.info("请先启动原神游戏，然后重新运行此测试")
    except Exception as e:
        logger = get_logger()
        logger.critical(f"测试脚本执行失败: {e}")
        print(f"测试脚本执行失败: {e}")

if __name__ == "__main__":
    test_window_switch()
