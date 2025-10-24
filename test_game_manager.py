"""
快速测试GameManager的screen_recognition属性
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game_manager import GameManager
from logger import get_logger


def test_game_manager_screen_recognition():
    """测试GameManager的screen_recognition属性"""
    try:
        logger = get_logger()
        logger.info("=== 测试GameManager screen_recognition属性 ===")
        
        # 创建游戏管理器实例
        game_manager = GameManager()
        
        # 检查screen_recognition属性是否存在
        if hasattr(game_manager, 'screen_recognition'):
            logger.info("✅ GameManager.screen_recognition 属性存在")
            
            # 检查screen_recognition的类型
            logger.info(f"screen_recognition 类型: {type(game_manager.screen_recognition)}")
            
            # 检查enter_game_template属性
            if hasattr(game_manager.screen_recognition, 'enter_game_template'):
                logger.info("✅ screen_recognition.enter_game_template 属性存在")
                if game_manager.screen_recognition.enter_game_template is not None:
                    logger.info(f"模板图片尺寸: {game_manager.screen_recognition.enter_game_template.shape}")
                else:
                    logger.info("模板图片未加载")
            else:
                logger.warning("❌ screen_recognition.enter_game_template 属性不存在")
            
            logger.info("✅ 测试通过！")
            return True
        else:
            logger.error("❌ GameManager.screen_recognition 属性不存在")
            return False
            
    except Exception as e:
        logger = get_logger()
        logger.critical(f"测试失败: {e}")
        print(f"测试失败: {e}")
        return False


if __name__ == "__main__":
    test_game_manager_screen_recognition()
