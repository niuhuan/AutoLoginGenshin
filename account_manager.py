"""
账号管理模块
使用与March7thAssistant相同的XOR加密方式保存账号和密码
"""
import base64
import os
import yaml
from pathlib import Path
from logger import get_logger

class AccountManager:
    def __init__(self):
        self.logger = get_logger()
        self.saved_accounts_dir = Path("saved_accounts")
        self.xor_key = "TI4ftRSDaP63kBxxoLoZ5KpVmRBz00JikzLNweryzZ4wecWJxJO9tbxlH9YDvjAr"
        
        # 确保目录存在
        self.saved_accounts_dir.mkdir(exist_ok=True)
    
    def xor_encrypt_to_base64(self, plaintext: str) -> str:
        """XOR加密并转换为base64"""
        secret_key = self.xor_key
        plaintext_bytes = plaintext.encode('utf-8')
        key_bytes = secret_key.encode('utf-8')

        encrypted_bytes = bytearray()
        for i in range(len(plaintext_bytes)):
            byte_plaintext = plaintext_bytes[i]
            byte_key = key_bytes[i % len(key_bytes)]
            encrypted_byte = byte_plaintext ^ byte_key
            encrypted_bytes.append(encrypted_byte)

        base64_encoded = base64.b64encode(encrypted_bytes).decode('utf-8')
        return base64_encoded

    def xor_decrypt_from_base64(self, encrypted_base64: str) -> str:
        """从base64解密XOR加密的内容"""
        secret_key = self.xor_key
        encrypted_bytes = base64.b64decode(encrypted_base64.encode('utf-8'))
        key_bytes = secret_key.encode('utf-8')

        decrypted_bytes = bytearray()
        for i in range(len(encrypted_bytes)):
            byte_encrypted = encrypted_bytes[i]
            byte_key = key_bytes[i % len(key_bytes)]
            decrypted_byte = byte_encrypted ^ byte_key
            decrypted_bytes.append(decrypted_byte)

        decrypted_str = decrypted_bytes.decode('utf-8')
        return decrypted_str

    def save_account(self, account_name: str, username: str, password: str) -> bool:
        """
        保存账号信息到文件
        
        Args:
            account_name: 账号名称
            username: 用户名
            password: 密码
            
        Returns:
            bool: 保存是否成功
        """
        try:
            # 加密账号和密码
            encrypted_credentials = self.xor_encrypt_to_base64(username + "," + password)
            
            # 创建简化的账号数据
            account_data = {
                'encrypted_credentials': encrypted_credentials
            }
            
            # 保存到YAML文件
            account_file = self.saved_accounts_dir / f"{account_name}.yaml"
            with open(account_file, 'w', encoding='utf-8') as f:
                yaml.dump(account_data, f, default_flow_style=False, allow_unicode=True)
            
            self.logger.info(f"✅ 账号 '{account_name}' 保存成功")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 保存账号失败: {e}")
            return False

    def load_account(self, account_name: str) -> tuple:
        """
        加载账号信息
        
        Args:
            account_name: 账号名称
            
        Returns:
            tuple: (username, password) 或 (None, None) 如果失败
        """
        try:
            account_file = self.saved_accounts_dir / f"{account_name}.yaml"
            
            if not account_file.exists():
                self.logger.warning(f"❌ 账号文件不存在: {account_file}")
                return None, None
            
            # 读取YAML文件
            with open(account_file, 'r', encoding='utf-8') as f:
                account_data = yaml.safe_load(f)
            
            # 解密账号和密码
            encrypted_credentials = account_data.get('encrypted_credentials')
            if not encrypted_credentials:
                self.logger.error(f"❌ 账号文件格式错误: {account_file}")
                return None, None
            
            decrypted_text = self.xor_decrypt_from_base64(encrypted_credentials)
            username, password = decrypted_text.split(",", 1)
            
            self.logger.info(f"✅ 账号 '{account_name}' 加载成功")
            return username, password
            
        except Exception as e:
            self.logger.error(f"❌ 加载账号失败: {e}")
            return None, None

    def list_accounts(self) -> list:
        """
        列出所有保存的账号
        
        Returns:
            list: 账号名称列表
        """
        try:
            accounts = []
            for file in self.saved_accounts_dir.glob("*.yaml"):
                account_name = file.stem
                accounts.append(account_name)
            return sorted(accounts)
        except Exception as e:
            self.logger.error(f"❌ 列出账号失败: {e}")
            return []

    def delete_account(self, account_name: str) -> bool:
        """
        删除账号
        
        Args:
            account_name: 账号名称
            
        Returns:
            bool: 删除是否成功
        """
        try:
            account_file = self.saved_accounts_dir / f"{account_name}.yaml"
            if account_file.exists():
                account_file.unlink()
                self.logger.info(f"✅ 账号 '{account_name}' 删除成功")
                return True
            else:
                self.logger.warning(f"❌ 账号文件不存在: {account_file}")
                return False
        except Exception as e:
            self.logger.error(f"❌ 删除账号失败: {e}")
            return False

    def account_exists(self, account_name: str) -> bool:
        """
        检查账号是否存在
        
        Args:
            account_name: 账号名称
            
        Returns:
            bool: 账号是否存在
        """
        account_file = self.saved_accounts_dir / f"{account_name}.yaml"
        return account_file.exists()
