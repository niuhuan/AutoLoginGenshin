"""
专门测试find_template_in_image方法的脚本
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game_manager import GameManager
from logger import get_logger
import cv2


def test_find_template_in_image():
    """测试find_template_in_image方法"""
    try:
        logger = get_logger()
        logger.info("=== 测试find_template_in_image方法 ===")
        
        # 创建游戏管理器实例
        game_manager = GameManager()
        
        # 测试1: 使用enter_game.png模板在need_login.png中匹配
        logger.info("测试1: 使用enter_game.png模板在need_login.png中匹配")
        
        # 加载模板图片
        template_path = os.path.join(os.path.dirname(__file__), 'assets', 'enter_game.png')
        if not os.path.exists(template_path):
            logger.warning(f"模板图片不存在: {template_path}")
            return False
        
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if template is None:
            logger.error("无法加载模板图片")
            return False
        
        logger.info(f"模板图片尺寸: {template.shape}")
        
        # 加载目标图片
        target_path = os.path.join(os.path.dirname(__file__), 'test_data', 'need_login.png')
        if not os.path.exists(target_path):
            logger.warning(f"目标图片不存在: {target_path}")
            return False
        
        target_image = cv2.imread(target_path, cv2.IMREAD_COLOR)
        if target_image is None:
            logger.error("无法加载目标图片")
            return False
        
        logger.info(f"目标图片尺寸: {target_image.shape}")
        
        # 测试不同的阈值
        thresholds = [0.5, 0.6, 0.7, 0.8, 0.9]
        
        for threshold in thresholds:
            logger.info(f"\n--- 测试阈值: {threshold} ---")
            
            # 调用抽象方法
            top_left, bottom_right, similarity = game_manager.find_template_in_image(
                target_image, template, threshold
            )
            
            if top_left is not None and bottom_right is not None:
                logger.info(f"✅ 找到匹配区域！")
                logger.info(f"匹配位置: {top_left} -> {bottom_right}")
                logger.info(f"相似度: {similarity:.3f}")
                
                # 保存结果图片
                try:
                    result_image = target_image.copy()
                    cv2.rectangle(result_image, top_left, bottom_right, (0, 255, 0), 2)
                    cv2.putText(result_image, f"Threshold: {threshold}, Match: {similarity:.3f}", 
                               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    
                    result_path = os.path.join(os.path.dirname(__file__), 'test_data', f'test_result_threshold_{threshold}.png')
                    cv2.imwrite(result_path, result_image)
                    logger.info(f"结果已保存到: {result_path}")
                except Exception as e:
                    logger.warning(f"保存结果失败: {e}")
            else:
                logger.info(f"❌ 未找到匹配区域")
                logger.info(f"最大相似度: {similarity:.3f}")
        
        # 测试2: 测试空参数
        logger.info("\n测试2: 测试空参数")
        
        # 测试空目标图片
        top_left, bottom_right, similarity = game_manager.find_template_in_image(
            None, template, 0.8
        )
        logger.info(f"空目标图片测试结果: {top_left}, {bottom_right}, {similarity}")
        
        # 测试空模板图片
        top_left, bottom_right, similarity = game_manager.find_template_in_image(
            target_image, None, 0.8
        )
        logger.info(f"空模板图片测试结果: {top_left}, {bottom_right}, {similarity}")
        
        # 测试3: 测试不同尺寸的图片
        logger.info("\n测试3: 测试不同尺寸的图片")
        
        # 创建一个小尺寸的测试图片
        small_image = cv2.resize(target_image, (200, 200))
        logger.info(f"小尺寸图片: {small_image.shape}")
        
        top_left, bottom_right, similarity = game_manager.find_template_in_image(
            small_image, template, 0.8
        )
        logger.info(f"小尺寸图片匹配结果: {top_left}, {bottom_right}, {similarity}")
        
        logger.info("=== 测试完成 ===")
        return True
        
    except Exception as e:
        logger = get_logger()
        logger.critical(f"测试失败: {e}")
        print(f"测试失败: {e}")
        return False


if __name__ == "__main__":
    test_find_template_in_image()
