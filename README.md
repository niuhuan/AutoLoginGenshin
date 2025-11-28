# 原神自动登录工具

一个用于自动启动和切换到原神游戏的Python工具，进行自动登录，支持uv开发环境和PyInstaller打包。

## 功能特性

- 🎮 自动检测原神游戏是否正在运行
- 🔄 如果游戏在运行则切换到游戏窗口，否则启动游戏
- ⌨ 检测有没有登录表单，有的话就提交登录，间隔60s，30s，30s。检测3次。

## 用户使用指南

### 解压和首次配置

1. **解压到单独文件夹**
   ```
   将下载的文件解压到一个单独的文件夹，例如：
   D:\AutoLoginGenshin\
   ```

2. **首次运行配置**
   ```powershell
   # 进入解压的文件夹
   cd D:\AutoLoginGenshin\
   
   # 运行程序（会自动获取管理员权限）
   .\AutoLoginGenshin.exe
   ```

3. **设置游戏路径**
   - 程序会自动打开配置界面
   - 点击"浏览"按钮选择 `YuanShen.exe` 文件
   - 点击"保存配置"保存设置

4. **保存账号信息**
   - 在"测试启动"区域输入账号和密码
   - 点击"另存为账号"按钮
   - 输入账号名称（如：account1）
   - 账号信息会加密保存到 `saved_accounts/` 目录

### 日常使用

配置完成后，可以使用以下方式启动：

```powershell
# 使用保存的账号自动登录
.\AutoLoginGenshin.exe --saved account1

# 直接输入账号密码
.\AutoLoginGenshin.exe -u 用户名 -p 密码
.\AutoLoginGenshin.exe --username 用户名 --password 密码
```


## 开发环境使用指南

### 开发环境设置

```powershell
# 1. 同步依赖（必须先运行）
.\dev_sync.ps1

# 2. 运行程序
.\dev_run.ps1 gui          # 显示配置界面
.\dev_run.ps1 run -u 用户名 -p 密码  # 命令行模式
.\dev_run.ps1 run --saved account1   # 使用保存的账号

# 3. 测试功能
.\dev_run.ps1 screen       # 测试屏幕识别
.\dev_run.ps1 login        # 测试自动登录
.\dev_run.ps1 template     # 测试模板匹配

# 4. 打包exe
.\dev_build.ps1            # 打包成exe文件
```

## 系统要求

- Windows 10/11
- 已安装的原神游戏
- 管理员权限（程序会自动请求）

## 其它

程序运行时会生成日志文件：
- `logs/genshin-auto-login.log`: 一般日志
- `logs/genshin-auto-login_error.log`: 错误日志

日志文件会按日期归档，最多保留30天。
