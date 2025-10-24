"""
配置文件管理模块
"""
import os
import yaml
from pathlib import Path


class ConfigManager:
    """配置文件管理器"""
    
    def __init__(self, config_filename="config.yaml"):
        """
        初始化配置管理器
        
        Args:
            config_filename: 配置文件名，默认为config.yaml
        """
        self.config_filename = config_filename
        self.config_path = self._get_config_path()
        self.config = self._load_config()
    
    def _get_config_path(self):
        """
        获取配置文件路径，确保与主程序在同一目录
        
        Returns:
            Path: 配置文件的完整路径
        """
        # 获取主程序所在目录
        if getattr(sys, 'frozen', False):
            # 如果是打包的exe文件
            base_dir = Path(sys.executable).parent
        else:
            # 如果是Python脚本
            base_dir = Path(__file__).parent
        
        config_path = base_dir / self.config_filename
        return config_path
    
    def _load_config(self):
        """
        加载配置文件
        
        Returns:
            dict: 配置数据
        """
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    return config if config is not None else {}
            else:
                # 配置文件不存在，创建默认配置
                self._create_default_config()
                return {}
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return {}
    
    def _create_default_config(self):
        """
        创建默认配置文件
        """
        try:
            default_config = {
                'yuan_shen_path': '',  # YuanShen.exe的完整路径
            }
            
            # 确保目录存在
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(default_config, f, default_flow_style=False, allow_unicode=True)
            
            print(f"已创建默认配置文件: {self.config_path}")
        except Exception as e:
            print(f"创建默认配置文件失败: {e}")
    
    def save_config(self, config_data=None):
        """
        保存配置到文件
        
        Args:
            config_data: 要保存的配置数据，如果为None则保存当前配置
            
        Returns:
            bool: 保存是否成功
        """
        try:
            if config_data is not None:
                self.config = config_data
            
            # 确保目录存在
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
            
            return True
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            return False
    
    def get(self, key, default=None):
        """
        获取配置值
        
        Args:
            key: 配置键
            default: 默认值
            
        Returns:
            配置值或默认值
        """
        return self.config.get(key, default)
    
    def set(self, key, value):
        """
        设置配置值
        
        Args:
            key: 配置键
            value: 配置值
        """
        self.config[key] = value
    
    def get_game_path(self):
        """
        获取游戏路径
        
        Returns:
            str: 游戏路径
        """
        return self.get('yuan_shen_path', '')
    
    def set_game_path(self, path):
        """
        设置游戏路径
        
        Args:
            path: 游戏路径
            
        Returns:
            bool: 设置是否成功
        """
        self.set('yuan_shen_path', path)
        return self.save_config()
    
    def validate_game_path(self, path):
        """
        验证游戏路径是否有效
        
        Args:
            path: 游戏路径
            
        Returns:
            tuple: (是否有效, 错误信息)
        """
        if not path:
            return False, "路径不能为空"
        
        if not os.path.exists(path):
            return False, "指定的文件不存在"
        
        if not path.endswith('YuanShen.exe'):
            return False, "请选择YuanShen.exe文件"
        
        return True, "路径有效"
    
    def get_config_path(self):
        """
        获取配置文件路径
        
        Returns:
            Path: 配置文件路径
        """
        return self.config_path
    
    def reload_config(self):
        """
        重新加载配置文件
        
        Returns:
            bool: 重新加载是否成功
        """
        self.config = self._load_config()
        return True


# 导入sys模块（在类外部）
import sys
