"""
快速测试修复后的test_screen_recognition.py
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from test_screen_recognition import template_matching_test
from logger import get_logger


def test_fix():
    """测试修复后的模板匹配功能"""
    try:
        logger = get_logger()
        logger.info("=== 测试修复后的模板匹配功能 ===")
        
        # 运行模板匹配测试
        result = template_matching_test()
        
        if result:
            logger.info("✅ 模板匹配测试成功！")
        else:
            logger.error("❌ 模板匹配测试失败")
        
        return result
        
    except Exception as e:
        logger = get_logger()
        logger.critical(f"测试失败: {e}")
        print(f"测试失败: {e}")
        return False


if __name__ == "__main__":
    test_fix()
