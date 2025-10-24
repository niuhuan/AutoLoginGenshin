# 原神自动登录工具

一个用于自动启动和切换到原神游戏的Python工具，支持uv开发环境和PyInstaller打包。

## 功能特性

- 🎮 自动检测原神游戏是否正在运行
- 🔄 如果游戏在运行则切换到游戏窗口，否则启动游戏
- ⚙️ 图形化配置界面设置游戏路径
- 📝 命令行参数支持
- 📁 YAML配置文件存储设置
- 🏗️ 模块化架构设计，GUI与逻辑分离
- 🔐 自动获取管理员权限
- 📦 支持uv开发环境和PyInstaller打包

## 项目结构

```
AutoLoginGenshin/
├── main.py              # 主程序入口
├── game_manager.py      # 核心游戏管理逻辑
├── gui.py              # GUI界面模块
├── admin_utils.py      # 管理员权限管理
├── config_manager.py   # 配置文件管理
├── account_manager.py      # 账号管理模块
├── logger.py           # 日志管理模块
├── screen_recognition.py # 屏幕识别模块
├── config.yaml         # 配置文件
├── pyproject.toml      # uv项目配置
├── .gitignore          # Git忽略文件
├── dev_setup.ps1       # 开发环境设置脚本
├── dev_sync.ps1        # 依赖同步脚本
├── dev_run.ps1         # 运行脚本
├── dev_build.ps1       # 打包exe脚本
├── test_window_switch.py    # 窗口切换测试
├── test_screen_recognition.py # 屏幕识别测试
├── test_template_matching.py # 模板匹配测试
├── test_auto_login.py      # 自动登录测试
├── test_account_manager.py # 账号管理测试
├── assets/             # 模板图片目录
│   ├── enter_game.png      # 进入游戏按钮模板
│   ├── circle.png          # 圆圈模板
│   ├── input_username.png  # 账号输入框模板
│   └── input_password.png  # 密码输入框模板
├── test_data/          # 测试数据目录
│   ├── need_login.png      # 测试用的登录界面图片
│   └── match_*.png         # 模板匹配结果图片
├── saved_accounts/     # 保存的账号目录（自动生成）
├── logs/               # 日志文件目录（自动生成）
├── uv/                 # 便携式uv目录（自动生成）
├── .venv/              # Python虚拟环境（自动生成）
└── README.md           # 使用说明
```

## 快速开始

### 一键设置开发环境

```powershell
# 1. 设置开发环境（自动安装uv，创建虚拟环境，安装依赖）
.\dev_setup.ps1

# 2. 同步依赖（可选，用于更新依赖）
.\dev_sync.ps1

# 3. 运行程序
.\dev_run.ps1

# 4. 打包exe文件（生成独立可执行文件）
.\dev_build.ps1
```

### 脚本使用说明

```powershell
# 运行程序
.\dev_run.ps1              # 运行程序（无参数时显示配置界面）
.\dev_run.ps1 run          # 运行程序
.\dev_run.ps1 gui          # 显示配置界面
.\dev_run.ps1 help         # 显示帮助信息

# 测试功能
.\dev_run.ps1 screen       # 测试屏幕识别功能
.\dev_run.ps1 login        # 测试自动登录功能
.\dev_run.ps1 template     # 测试模板匹配功能

# 命令行参数
.\dev_run.ps1 run -u 用户名 -p 密码  # 命令行模式启动
.\dev_run.ps1 run --saved account1   # 使用保存的账号

# 打包exe（生成独立可执行文件，无需Python环境）
.\dev_build.ps1            # 打包成exe文件
```

## 使用方法

### 1. 首次配置

直接运行程序（无参数）会打开图形化配置界面：

```bash
uv run python main.py
```

在配置界面中：
- 点击"浏览"按钮选择YuanShen.exe文件
- 点击"保存配置"保存设置
- 点击"测试启动"验证配置是否正确

### 2. 命令行使用

配置完成后，可以使用命令行参数：

```bash
# 使用保存的账号
uv run python main.py --saved account1

# 直接输入账号密码
uv run python main.py --username "用户名" --password "密码"
uv run python main.py -u "用户名" -p "密码"
```

### 3. 打包后的exe使用

打包完成后，在 `dist/` 目录下会生成 `GenshinAutoLogin.exe` 文件：

```bash
# 首次运行（配置模式）
dist/GenshinAutoLogin.exe

# 直接启动游戏
dist/GenshinAutoLogin.exe --open
```

## 模块说明

### game_manager.py
- `GameManager` 类：核心游戏管理逻辑
- 配置文件管理
- 游戏进程检测
- 窗口切换和游戏启动

### gui.py
- `ConfigWindow` 类：配置界面
- 文件浏览对话框
- 配置保存和加载
- 测试启动功能

### admin_utils.py
- `is_admin()`: 检查管理员权限
- `run_as_admin()`: 请求管理员权限
- `check_and_request_admin()`: 检查并请求权限
- `create_manifest()`: 创建应用程序清单

### main.py
- 命令行参数解析
- 程序入口点
- GUI和命令行模式切换
- 管理员权限检查

### build.py
- PyInstaller打包配置
- 自动生成应用程序清单
- 依赖库隐藏导入配置

## 配置文件

程序会在当前目录创建 `config.yaml` 配置文件：

```yaml
yuan_shen_path: "C:\Program Files\Genshin Impact\Genshin Impact Game\YuanShen.exe"
```

## 工作原理

1. **权限检查**: 程序启动时自动检查管理员权限，如无权限则请求提升
2. **游戏检测**: 使用 `psutil` 库检测YuanShen.exe进程是否在运行
3. **窗口切换**: 使用 `pywin32` 库查找并切换到游戏窗口
4. **游戏启动**: 使用 `subprocess` 启动游戏进程
5. **配置管理**: 使用 `PyYAML` 库管理配置文件
6. **模块化设计**: GUI界面与核心逻辑完全分离
7. **打包优化**: 使用PyInstaller打包成单个exe文件，包含所有依赖

## 开发说明

### uv环境管理

```bash
# 安装开发依赖
uv pip install -e ".[dev]"

# 运行代码格式化
uv run black .

# 运行代码检查
uv run flake8 .

# 运行测试
uv run pytest
```

### PyInstaller打包

打包脚本会自动：
- 创建应用程序清单文件请求管理员权限
- 隐藏所有必要的依赖库导入
- 包含配置文件到exe中
- 生成单个可执行文件

## 开发环境说明

### 智能环境管理
- ✅ **自动检测uv**: 优先使用全局uv，失败时自动安装便携式uv
- ✅ **环境变量设置**: 自动设置便携式uv的环境变量
- ✅ **虚拟环境管理**: 自动创建和管理Python虚拟环境
- ✅ **依赖同步**: 使用uv sync进行高效的依赖管理
- ✅ **便携式支持**: 支持便携式安装，整个文件夹可复制使用

### 脚本功能说明

#### dev_setup.bat
- 检查并安装uv（全局优先，失败时便携式安装）
- 创建Python虚拟环境
- 安装项目依赖
- 自动设置环境变量

#### dev_sync.bat
- 同步项目依赖（使用uv sync）
- 显示环境信息
- 检查依赖状态

#### dev_run.bat
- 运行程序（支持多种模式）
- 显示帮助信息
- 支持命令行参数传递
- 测试窗口切换功能 (`dev_run.bat test`)
- 测试屏幕识别功能 (`dev_run.bat screen`)

#### 屏幕识别测试功能
- **模板图片**: 使用 `assets/enter_game.png` 作为匹配模板
- **目标图片**: 在 `test_data/need_login.png` 中寻找匹配区域
- **功能**: 使用cv2模板匹配判断是否为登录界面
- **使用方法**: `dev_run.bat screen`
- **输出**: 显示匹配结果、相似度和匹配位置
- **结果保存**: 自动保存匹配结果图片到 `test_data/template_match_result.png`

#### dev_build.bat
- 打包exe文件（生成独立可执行文件）
- 自动安装PyInstaller
- 创建应用程序清单文件
- 包含所有依赖库
- 清理临时文件

### 便携式安装后的目录结构
```
AutoLoginGenshin/
├── uv/                    # 便携式uv工具（如果全局安装失败）
│   └── uv.exe
├── .venv/                 # Python虚拟环境
│   ├── Scripts/
│   ├── Lib/
│   └── pyvenv.cfg
├── dev_setup.bat          # 环境设置脚本
├── dev_sync.bat           # 依赖同步脚本
├── dev_run.bat            # 运行脚本
├── dev_build.bat          # 打包脚本
└── ... (其他项目文件)
```

## 自动登录功能

### 功能概述
- 🎯 **智能识别**: 自动检测登录界面
- ⌨️ **自动输入**: 自动输入账号密码
- 🔄 **输入法切换**: 自动切换至英文输入法
- 🖱️ **智能点击**: 自动点击登录相关按钮

### 技术实现
基于March7thAssistant的登录机制：
- **输入法管理**: 使用`win32api`确保输入法为英文
- **键盘模拟**: 使用`pyautogui`模拟键盘输入
- **图像识别**: 使用`cv2`模板匹配识别登录界面元素
- **坐标点击**: 智能定位并点击输入框和按钮

### 使用方法
```powershell
# 命令行模式（自动登录）
.\dev_run.ps1 run -u 用户名 -p 密码

# 使用保存的账号
.\dev_run.ps1 run --saved account1

# GUI模式（手动输入账号密码）
.\dev_run.ps1 gui
```

### 账号管理功能
- **保存账号**: 在GUI中点击"另存为账号"按钮，输入账号名称保存当前账号密码
- **加密存储**: 使用与March7thAssistant相同的XOR加密方式保存账号信息
- **文件位置**: 账号文件保存在 `saved_accounts/` 目录下，格式为 `账号名.yaml`
- **命令行使用**: 支持 `--saved 账号名` 参数直接使用保存的账号登录
- **安全特性**: 账号密码经过XOR加密和Base64编码，确保安全性
- **简化配置**: 配置文件只包含 `encrypted_credentials` 字段，结构简洁

### 测试功能
```powershell
# 测试自动登录功能
.\dev_run.ps1 login

# 测试屏幕识别
.\dev_run.ps1 screen

# 测试模板匹配
.\dev_run.ps1 template
```

### 登录流程
1. **检测圆圈**: 使用`circle.png`模板检测并点击可能的加载圆圈
2. **检测登录界面**: 使用`enter_game.png`模板识别登录界面
3. **点击进入游戏**: 如果检测到进入游戏按钮，自动点击
4. **智能输入账号**: 使用`input_username.png`模板精确匹配账号输入框位置并点击
5. **智能输入密码**: 使用`input_password.png`模板精确匹配密码输入框位置并点击
6. **点击登录**: 点击登录按钮完成登录
7. **再次点击进入游戏**: 登录完成后再次点击进入游戏按钮
8. **程序退出**: 登录流程完成后程序自动退出

### 注意事项
- 账号和密码输入框使用模板匹配精确定位（无需手动调整坐标）
- 登录按钮仍使用固定坐标（可根据需要添加模板匹配）
- 自动登录完成后程序会自动退出，无需手动关闭
- exe文件已修复OpenCV配置问题和命令行参数问题，可以正常运行
- 建议先使用`.\dev_run.ps1 screen`测试模板匹配
- 建议先使用`.\dev_run.ps1 login`测试自动登录功能
- 如果登录失败，请检查游戏界面布局是否发生变化
- 支持中文和英文用户名密码输入
- 自动检测并点击加载圆圈，提高登录成功率
- **智能切换**: 如果原神游戏已在运行，会直接切换到游戏窗口；如果游戏未运行，会启动游戏

## 系统要求

- Windows 10/11
- Python 3.8+（便携式安装会自动下载）
- 已安装的原神游戏
- 管理员权限（程序会自动请求）

## 注意事项

- 首次使用需要手动配置游戏路径
- 程序会自动请求管理员权限以正常启动游戏
- 确保有足够的权限启动游戏
- 如果游戏路径发生变化，需要重新配置
- 打包的exe文件需要管理员权限运行

## 清华源配置

### 为什么使用清华源？
- 🚀 **下载速度**: 清华源在国内访问速度更快
- 📦 **依赖安装**: 特别是OpenCV等大型依赖包
- 🔧 **开发效率**: 减少等待时间，提高开发效率

### 配置方法

#### 方法1: 使用配置脚本（推荐）
```bash
# 运行清华源配置脚本
dev_config_mirror.bat
```

#### 方法2: 手动配置
```bash
# 设置清华源
uv pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
uv pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn

# 查看当前配置
uv pip config list
```

#### 方法3: 临时使用清华源
```bash
# 单次安装时指定清华源
uv pip install -i https://pypi.tuna.tsinghua.edu.cn/simple opencv-python
```

### 验证配置
```bash
# 查看当前pip配置
uv pip config list

# 测试下载速度
uv pip install --dry-run opencv-python
```

### 其他镜像源
如果清华源不稳定，可以尝试其他镜像源：

```bash
# 阿里云镜像
uv pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/

# 豆瓣镜像
uv pip config set global.index-url https://pypi.douban.com/simple/

# 中科大镜像
uv pip config set global.index-url https://pypi.mirrors.ustc.edu.cn/simple/
```
