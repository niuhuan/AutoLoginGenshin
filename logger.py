"""
日志管理模块
"""
import os
import logging
import logging.handlers
from datetime import datetime, timedelta
import sys


class Logger:
    """日志管理器"""
    
    def __init__(self, name="genshin-auto-login"):
        self.name = name
        self.logger = None
        self.log_dir = self._get_log_directory()
        self._setup_logger()
    
    def _get_log_directory(self):
        """获取日志目录"""
        if getattr(sys, 'frozen', False):
            # 如果是打包的exe文件
            exe_dir = os.path.dirname(sys.executable)
            log_dir = os.path.join(exe_dir, "logs")
        else:
            # 如果是Python脚本
            script_dir = os.path.dirname(os.path.abspath(__file__))
            log_dir = os.path.join(script_dir, "logs")
        
        # 创建logs目录
        os.makedirs(log_dir, exist_ok=True)
        return log_dir
    
    def _setup_logger(self):
        """设置日志器"""
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)
        
        # 避免重复添加处理器
        if self.logger.handlers:
            return
        
        # 创建格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # 文件处理器 - 按日期轮转
        log_file = os.path.join(self.log_dir, f"{self.name}.log")
        file_handler = logging.handlers.TimedRotatingFileHandler(
            filename=log_file,
            when='midnight',
            interval=1,
            backupCount=30,  # 保留30天
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # 错误日志文件处理器
        error_log_file = os.path.join(self.log_dir, f"{self.name}_error.log")
        error_handler = logging.handlers.TimedRotatingFileHandler(
            filename=error_log_file,
            when='midnight',
            interval=1,
            backupCount=30,  # 保留30天
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        self.logger.addHandler(error_handler)
    
    def debug(self, message):
        """调试日志"""
        self.logger.debug(message)
    
    def info(self, message):
        """信息日志"""
        self.logger.info(message)
    
    def warning(self, message):
        """警告日志"""
        self.logger.warning(message)
    
    def error(self, message):
        """错误日志"""
        self.logger.error(message)
    
    def critical(self, message):
        """严重错误日志"""
        self.logger.critical(message)
    
    def cleanup_old_logs(self):
        """清理超过30天的旧日志文件"""
        try:
            cutoff_date = datetime.now() - timedelta(days=30)
            log_files = []
            
            # 收集所有日志文件
            for filename in os.listdir(self.log_dir):
                if filename.startswith(self.name) and filename.endswith('.log'):
                    log_files.append(filename)
            
            # 检查并删除过期文件
            for filename in log_files:
                file_path = os.path.join(self.log_dir, filename)
                try:
                    file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if file_time < cutoff_date:
                        os.remove(file_path)
                        if self.logger:
                            self.logger.info(f"已删除过期日志文件: {filename}")
                except Exception as e:
                    if self.logger:
                        self.logger.error(f"删除日志文件失败 {filename}: {e}")
                    
        except Exception as e:
            if self.logger:
                self.logger.error(f"清理日志文件失败: {e}")
            else:
                print(f"清理日志文件失败: {e}")


# 全局日志器实例
logger = Logger()


def get_logger():
    """获取日志器实例"""
    return logger


def log_debug(message):
    """调试日志"""
    logger.debug(message)


def log_info(message):
    """信息日志"""
    logger.info(message)


def log_warning(message):
    """警告日志"""
    logger.warning(message)


def log_error(message):
    """错误日志"""
    logger.error(message)


def log_critical(message):
    """严重错误日志"""
    logger.critical(message)


def cleanup_logs():
    """清理旧日志"""
    logger.cleanup_old_logs()


if __name__ == "__main__":
    # 测试日志功能
    logger = get_logger()
    
    logger.info("日志系统测试开始")
    logger.debug("这是一条调试信息")
    logger.warning("这是一条警告信息")
    logger.error("这是一条错误信息")
    
    print(f"日志目录: {logger.log_dir}")
    print("日志测试完成")
