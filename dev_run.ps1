# 原神自动登录工具 - 运行脚本
# ============================

# 设置控制台编码为UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# 设置项目根目录
$PROJECT_ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $PROJECT_ROOT

Write-Host "原神自动登录工具 - 运行脚本" -ForegroundColor Green
Write-Host "============================" -ForegroundColor Green

# 检查uv是否可用
if (Test-Path "$PROJECT_ROOT\uv\uv.exe") {
    Write-Host "使用便携式uv环境..." -ForegroundColor Yellow
    $UV_EXE = "$PROJECT_ROOT\uv\uv.exe"
    $env:PATH = "$PROJECT_ROOT\uv;$env:PATH"
} else {
    Write-Host "使用全局uv环境..." -ForegroundColor Yellow
    # 尝试多种方式找到uv
    try {
        & uv --version | Out-Null
        if ($LASTEXITCODE -eq 0) {
            $UV_EXE = "uv"
        } else {
            throw "uv not found"
        }
    } catch {
        try {
            $uvPath = Get-Command uv -ErrorAction Stop
            $UV_EXE = "uv"
        } catch {
            Write-Host "[ERROR] uv未安装，请先运行 dev_setup.ps1" -ForegroundColor Red
            exit 1
        }
    }
}

# 检查虚拟环境是否存在
if (-not (Test-Path "$PROJECT_ROOT\.venv")) {
    Write-Host "[ERROR] 虚拟环境不存在，请先运行 dev_setup.ps1" -ForegroundColor Red
    exit 1
}

# 定义帮助函数
function Show-Help {
    Write-Host ""
    Write-Host "使用方法:" -ForegroundColor Yellow
    Write-Host "  dev_run.ps1           - 运行程序（无参数时显示配置界面）" -ForegroundColor White
    Write-Host "  dev_run.ps1 run       - 运行程序" -ForegroundColor White
    Write-Host "  dev_run.ps1 gui       - 显示配置界面" -ForegroundColor White
    Write-Host "  dev_run.ps1 test      - 测试窗口切换功能" -ForegroundColor White
    Write-Host "  dev_run.ps1 screen    - 使用enter_game.png模板匹配测试" -ForegroundColor White
    Write-Host "  dev_run.ps1 template  - 测试find_template_in_image方法" -ForegroundColor White
    Write-Host "  dev_run.ps1 login     - 测试自动登录功能" -ForegroundColor White
    Write-Host "  dev_run.ps1 build     - 打包exe文件" -ForegroundColor White
    Write-Host "  dev_run.ps1 help      - 显示帮助信息" -ForegroundColor White
    Write-Host ""
    Write-Host "命令行参数:" -ForegroundColor Yellow
    Write-Host "  dev_run.ps1 run -o -u 用户名 -p 密码  - 命令行模式启动（必须提供用户名和密码）" -ForegroundColor White
    Write-Host "  dev_run.ps1 run -u 用户名 -p 密码     - 带用户名密码启动（可选）" -ForegroundColor White
    Write-Host ""
}

# 解析命令行参数
$COMMAND = $args[0]
if (-not $COMMAND) { $COMMAND = "run" }

switch ($COMMAND) {
    "run" { 
        Write-Host "启动原神自动登录工具..." -ForegroundColor Cyan
        & $UV_EXE run python main.py $args[1..($args.Length-1)]
    }
    "build" { 
        Write-Host "打包exe文件..." -ForegroundColor Cyan
        & $UV_EXE run python build.py
        if ($LASTEXITCODE -eq 0) {
            Write-Host "打包完成！" -ForegroundColor Green
        } else {
            Write-Host "打包失败！" -ForegroundColor Red
        }
    }
    "gui" { 
        Write-Host "显示配置界面..." -ForegroundColor Cyan
        & $UV_EXE run python main.py
    }
    "test" { 
        Write-Host "测试窗口切换功能..." -ForegroundColor Cyan
        & $UV_EXE run python test_window_switch.py
    }
    "screen" { 
        Write-Host "测试屏幕识别功能..." -ForegroundColor Cyan
        & $UV_EXE run python test_screen_recognition.py
    }
    "template" { 
        Write-Host "测试模板匹配方法..." -ForegroundColor Cyan
        & $UV_EXE run python test_template_matching.py
    }
    "login" { 
        Write-Host "测试自动登录功能..." -ForegroundColor Cyan
        & $UV_EXE run python test_auto_login.py
    }
    "help" { 
        Show-Help
    }
    default { 
        Write-Host "启动原神自动登录工具..." -ForegroundColor Cyan
        & $UV_EXE run python main.py $args
    }
}
