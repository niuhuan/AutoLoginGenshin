"""
原神自动登录工具主程序
"""
import sys
import argparse
from game_manager import GameManager
from gui import show_config_window
from admin_utils import check_and_request_admin
from account_manager import AccountManager
from logger import get_logger, cleanup_logs


def main():
    """主函数"""
    try:
        # 初始化日志系统
        logger = get_logger()
        logger.info("原神自动登录工具启动")
        
        # 清理旧日志
        cleanup_logs()
        
        # 检查并请求管理员权限
        if not check_and_request_admin():
            logger.error("无法获取管理员权限，程序退出")
            sys.exit(1)
        
        parser = argparse.ArgumentParser(description='原神自动登录工具')
        parser.add_argument('--open', '-o', action='store_true', help='直接打开游戏并登录而非显示GUI')
        parser.add_argument('--username', '-u', type=str, help='用户名')
        parser.add_argument('--password', '-p', type=str, help='密码')
        parser.add_argument('--saved', type=str, help='使用保存的账号名称')
        
        args = parser.parse_args()
        
        # 创建游戏管理器实例
        game_manager = GameManager()
        account_manager = AccountManager()
        
        # 如果有命令行参数，则不显示GUI
        if args.username or args.password or args.saved:
            logger.info("命令行模式启动")
            
            # 处理保存的账号
            username = args.username
            password = args.password
            
            if args.saved:
                logger.info(f"使用保存的账号: {args.saved}")
                loaded_username, loaded_password = account_manager.load_account(args.saved)
                if loaded_username and loaded_password:
                    username = loaded_username
                    password = loaded_password
                    logger.info(f"✅ 账号 '{args.saved}' 加载成功")
                else:
                    logger.error(f"❌ 无法加载账号 '{args.saved}'")
                    sys.exit(1)
            
            # 如果有用户名，就执行登录
            if username and password:
                # 使用统一的登录处理方法
                success = game_manager.handle_login(username=username, password=password)
                if not success:
                    logger.error("游戏启动失败")
                    sys.exit(1)
            else:
                logger.error("必须提供账号密码（通过 -u/-p 或 --saved）")
                print("错误: 必须提供账号密码")
                print("示例: dev_run.bat run -u 用户名 -p 密码")
                print("或: dev_run.bat run --saved account1")
                sys.exit(1)
        else:
            logger.info("GUI模式启动")
            # 没有参数时显示GUI配置界面
            show_config_window()
            
    except KeyboardInterrupt:
        logger.info("用户中断程序")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"程序发生未处理的异常: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
