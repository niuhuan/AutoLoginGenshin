"""
屏幕识别测试脚本 - 测试多个模板的匹配结果
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logger import get_logger
from game_manager import GameManager
import cv2
import numpy as np


def multi_template_matching_test():
    """测试多个模板的匹配结果"""
    try:
        logger = get_logger()
        logger.info("=== 多模板匹配测试 ===")
        
        # 创建游戏管理器实例
        game_manager = GameManager()
        
        # 定义要测试的模板
        templates = [
            {
                'name': '进入游戏按钮',
                'path': 'assets/enter_game.png',
                'threshold': 0.8,
                'description': '检测登录界面的进入游戏按钮'
            },
            {
                'name': '圆圈',
                'path': 'assets/circle.png',
                'threshold': 0.7,
                'description': '检测可能的加载圆圈或按钮'
            },
            {
                'name': '账号输入框',
                'path': 'assets/input_username.png',
                'threshold': 0.7,
                'description': '检测账号输入框位置'
            },
            {
                'name': '密码输入框',
                'path': 'assets/input_password.png',
                'threshold': 0.7,
                'description': '检测密码输入框位置'
            }
        ]
        
        # 目标图片路径
        target_image_path = os.path.join(os.path.dirname(__file__), 'test_data', 'need_login.png')
        logger.info(f"目标图片路径: {target_image_path}")
        
        if not os.path.exists(target_image_path):
            logger.warning(f"目标图片不存在: {target_image_path}")
            logger.info("请确保 test_data/need_login.png 文件存在")
            return False
        
        # 加载目标图片
        logger.info("加载目标图片...")
        target_image = cv2.imread(target_image_path, cv2.IMREAD_COLOR)
        if target_image is None:
            logger.error("无法加载目标图片")
            return False
        
        logger.info(f"目标图片尺寸: {target_image.shape}")
        
        # 测试每个模板
        results = []
        for template_info in templates:
            logger.info(f"\n--- 测试模板: {template_info['name']} ---")
            logger.info(f"描述: {template_info['description']}")
            
            template_path = os.path.join(os.path.dirname(__file__), template_info['path'])
            logger.info(f"模板路径: {template_path}")
            
            if not os.path.exists(template_path):
                logger.warning(f"模板图片不存在: {template_path}")
                continue
            
            # 加载模板图片
            template = cv2.imread(template_path, cv2.IMREAD_COLOR)
            if template is None:
                logger.error(f"无法加载模板图片: {template_path}")
                continue
            
            logger.info(f"模板图片尺寸: {template.shape}")
            
            # 进行模板匹配
            logger.info(f"开始模板匹配，阈值: {template_info['threshold']}")
            
            top_left, bottom_right, similarity = game_manager.find_template_in_image(
                target_image, template, template_info['threshold']
            )
            
            result = {
                'name': template_info['name'],
                'path': template_info['path'],
                'threshold': template_info['threshold'],
                'similarity': similarity,
                'found': top_left is not None,
                'position': (top_left, bottom_right) if top_left is not None else None
            }
            results.append(result)
            
            if top_left is not None and bottom_right is not None:
                logger.info("✅ 找到匹配区域！")
                logger.info(f"匹配位置: {top_left} -> {bottom_right}")
                logger.info(f"匹配区域尺寸: {template.shape[1]}x{template.shape[0]}")
                logger.info(f"相似度: {similarity:.3f}")
                
                # 保存匹配结果图片
                try:
                    result_image = target_image.copy()
                    cv2.rectangle(result_image, top_left, bottom_right, (0, 255, 0), 2)
                    
                    # 在匹配区域添加文字标注
                    cv2.putText(result_image, f"{template_info['name']}: {similarity:.3f}", 
                                (top_left[0], top_left[1] - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    
                    # 保存结果图片（使用英文文件名避免乱码）
                    safe_name = template_info["name"].replace("进入游戏按钮", "enter_game").replace("圆圈", "circle").replace("账号输入框", "username_input").replace("密码输入框", "password_input")
                    result_path = os.path.join(os.path.dirname(__file__), 'test_data', f'match_{safe_name}_result.png')
                    cv2.imwrite(result_path, result_image)
                    logger.info(f"匹配结果已保存到: {result_path}")
                    
                except Exception as e:
                    logger.warning(f"保存匹配结果失败: {e}")
                
            else:
                logger.info("❌ 未找到匹配区域")
                logger.info(f"最大相似度 {similarity:.3f} < 阈值 {template_info['threshold']}")
        
        # 输出总结
        logger.info("\n=== 匹配结果总结 ===")
        for result in results:
            status = "✅ 找到" if result['found'] else "❌ 未找到"
            logger.info(f"{result['name']}: {status} (相似度: {result['similarity']:.3f})")
        
        # 判断是否为登录界面
        enter_game_found = any(r['name'] == '进入游戏按钮' and r['found'] for r in results)
        circle_found = any(r['name'] == '圆圈' and r['found'] for r in results)
        username_found = any(r['name'] == '账号输入框' and r['found'] for r in results)
        password_found = any(r['name'] == '密码输入框' and r['found'] for r in results)
        
        logger.info(f"\n=== 界面判断 ===")
        if enter_game_found:
            logger.info("🎯 结论: 这是登录界面（检测到进入游戏按钮）")
        elif username_found and password_found:
            logger.info("🎯 结论: 这是登录界面（检测到账号和密码输入框）")
        elif username_found or password_found:
            logger.info("🎯 结论: 检测到部分登录界面元素")
        elif circle_found:
            logger.info("🎯 结论: 检测到圆圈，可能是加载界面")
        else:
            logger.info("🎯 结论: 未检测到登录界面特征")
        
        logger.info("=== 多模板匹配测试完成 ===")
        return True
        
    except Exception as e:
        logger = get_logger()
        logger.critical(f"多模板匹配测试失败: {e}")
        print(f"多模板匹配测试失败: {e}")
        return False


if __name__ == "__main__":
    multi_template_matching_test()