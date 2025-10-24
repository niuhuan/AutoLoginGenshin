"""
原神自动登录工具GUI界面模块
"""
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                            QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, 
                            QGroupBox, QInputDialog, QMessageBox)
from PyQt5.QtCore import Qt
from game_manager import GameManager
from config_manager import ConfigManager
from account_manager import AccountManager
from logger import get_logger


class ConfigWindow(QMainWindow):
    """配置窗口类"""
    
    def __init__(self):
        super().__init__()
        self.game_manager = GameManager()
        self.config_manager = ConfigManager()
        self.account_manager = AccountManager()
        self.logger = get_logger()
        self.init_ui()
        self.load_config()
    
    def init_ui(self):
        """初始化UI界面"""
        self.setWindowTitle("原神自动登录工具 - 配置")
        self.setFixedSize(500, 400)
        
        # 主窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 布局
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 设置组
        settings_group = QGroupBox("设置")
        settings_layout = QVBoxLayout()
        settings_group.setLayout(settings_layout)
        
        # 路径输入
        path_input_layout = QHBoxLayout()
        path_input_layout.addWidget(QLabel("YuanShen.exe 路径:"))
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("请选择YuanShen.exe文件...")
        path_input_layout.addWidget(self.path_input)
        
        # 浏览按钮
        browse_btn = QPushButton("浏览")
        browse_btn.clicked.connect(self.browse_file)
        path_input_layout.addWidget(browse_btn)
        
        settings_layout.addLayout(path_input_layout)
        
        layout.addWidget(settings_group)
        
        # 测试启动组
        test_group = QGroupBox("测试启动")
        test_layout = QVBoxLayout()
        test_group.setLayout(test_layout)
        
        # 账号密码输入
        username_layout = QHBoxLayout()
        username_layout.addWidget(QLabel("账号:"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("请输入账号...")
        username_layout.addWidget(self.username_input)
        test_layout.addLayout(username_layout)
        
        password_layout = QHBoxLayout()
        password_layout.addWidget(QLabel("密码:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("请输入密码...")
        password_layout.addWidget(self.password_input)
        test_layout.addLayout(password_layout)
        
        # 测试启动按钮
        test_btn = QPushButton("测试启动")
        test_btn.clicked.connect(self.test_launch)
        test_layout.addWidget(test_btn)
        
        # 另存为账号按钮
        save_account_btn = QPushButton("另存为账号")
        save_account_btn.clicked.connect(self.save_account)
        test_layout.addWidget(save_account_btn)
        
        layout.addWidget(test_group)
    
    def browse_file(self):
        """浏览文件对话框"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择YuanShen.exe", "", "可执行文件 (*.exe)"
        )
        if file_path:
            self.path_input.setText(file_path)
            # 自动保存配置
            self.auto_save_config(file_path)
    
    def auto_save_config(self, file_path):
        """自动保存配置"""
        try:
            # 验证路径
            is_valid, message = self.config_manager.validate_game_path(file_path)
            if not is_valid:
                QMessageBox.warning(self, "路径无效", message)
                return False
            
            # 保存游戏路径
            self.config_manager.set_game_path(file_path)
            QMessageBox.information(self, "保存成功", "游戏路径已自动保存")
            self.logger.info("游戏路径已自动保存")
            return True
        except Exception as e:
            QMessageBox.critical(self, "保存失败", f"保存配置失败: {e}")
            self.logger.error(f"自动保存配置失败: {e}")
            return False
    
    def load_config(self):
        """加载配置到界面"""
        try:
            # 加载游戏路径
            game_path = self.config_manager.get_game_path()
            if game_path:
                self.path_input.setText(game_path)
        except Exception as e:
            self.logger.error(f"加载配置文件失败: {e}")
    
    def save_config(self):
        """保存配置"""
        path = self.path_input.text().strip()
        
        # 验证路径
        is_valid, message = self.config_manager.validate_game_path(path)
        if not is_valid:
            self.logger.warning(message)
            return

        try:
            # 保存游戏路径
            self.config_manager.set_game_path(path)
            self.logger.info("配置已保存")
        except Exception as e:
            self.logger.error(f"保存配置失败: {e}")
    
    def test_launch(self):
        """测试启动游戏"""
        path = self.path_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        # 验证路径
        is_valid, message = self.config_manager.validate_game_path(path)
        if not is_valid:
            QMessageBox.warning(self, "路径无效", message)
            return

        # 验证账号密码
        if not username:
            QMessageBox.warning(self, "输入错误", "请输入账号")
            return

        if not password:
            QMessageBox.warning(self, "输入错误", "请输入密码")
            return
        
        # 显示测试启动提示
        reply = QMessageBox.question(
            self, '测试启动', 
            f'即将使用账号 "{username}" 启动游戏，是否继续？',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        # 使用统一的登录处理方法
        success = self.game_manager.handle_login(username=username, password=password, game_path=path)
        
        if success:
            QMessageBox.information(self, "启动成功", "游戏启动成功！")
            self.logger.info("✅ 测试启动成功！")
        else:
            QMessageBox.critical(self, "启动失败", "游戏启动失败，请检查配置")
            self.logger.error("❌ 测试启动失败")
    
    def save_account(self):
        """保存账号"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        # 验证账号密码
        if not username:
            QMessageBox.warning(self, "输入错误", "请输入账号")
            return

        if not password:
            QMessageBox.warning(self, "输入错误", "请输入密码")
            return
        
        # 获取账号名称
        account_name, ok = QInputDialog.getText(
            self, '另存为账号', '请输入账号名称:', 
            text=f"account_{username[:10]}"  # 默认使用账号前10位
        )
        
        if not ok or not account_name.strip():
            return
        
        account_name = account_name.strip()
        
        # 检查账号是否已存在
        if self.account_manager.account_exists(account_name):
            reply = QMessageBox.question(
                self, '账号已存在', 
                f'账号 "{account_name}" 已存在，是否覆盖？',
                QMessageBox.Yes | QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return
        
        # 保存账号
        success = self.account_manager.save_account(account_name, username, password)
        
        if success:
            QMessageBox.information(self, "保存成功", f"账号 '{account_name}' 保存成功！")
            self.logger.info(f"✅ 账号 '{account_name}' 保存成功！")
        else:
            QMessageBox.critical(self, "保存失败", f"账号 '{account_name}' 保存失败")
            self.logger.error(f"❌ 账号 '{account_name}' 保存失败")


def show_config_window():
    """显示配置窗口"""
    try:
        app = QApplication(sys.argv)
        window = ConfigWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        logger = get_logger()
        logger.critical(f"GUI启动失败: {e}")
        print(f"GUI启动失败: {e}")
        sys.exit(1)
