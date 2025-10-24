# 原神自动登录工具 - 同步依赖
# ============================

# 设置控制台编码为UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# 设置项目根目录
$PROJECT_ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $PROJECT_ROOT

Write-Host "原神自动登录工具 - 同步依赖" -ForegroundColor Green
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

Write-Host "同步项目依赖..." -ForegroundColor Cyan

# 配置清华源
Write-Host "配置清华源..." -ForegroundColor Yellow
& $UV_EXE pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
& $UV_EXE pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn

# 安装核心依赖
Write-Host "安装核心依赖..." -ForegroundColor Yellow
& $UV_EXE pip install PyQt5 psutil pywin32 pyinstaller pyyaml

# 安装开发依赖
Write-Host "安装开发依赖..." -ForegroundColor Yellow
& $UV_EXE pip install opencv-python pillow pyautogui

# 安装屏幕识别依赖
Write-Host "安装屏幕识别依赖..." -ForegroundColor Yellow
& $UV_EXE pip install numpy

Write-Host "依赖同步完成！" -ForegroundColor Green
