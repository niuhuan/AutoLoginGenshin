# 原神自动登录工具 - 环境设置
# ============================

# 设置控制台编码为UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# 设置项目根目录
$PROJECT_ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $PROJECT_ROOT

Write-Host "原神自动登录工具 - 环境设置" -ForegroundColor Green
Write-Host "============================" -ForegroundColor Green

# 检查是否已存在便携式uv
if (Test-Path "$PROJECT_ROOT\uv\uv.exe") {
    Write-Host "便携式uv已存在，跳过安装..." -ForegroundColor Yellow
} else {
    Write-Host "安装便携式uv..." -ForegroundColor Cyan
    
    # 创建uv目录
    if (-not (Test-Path "$PROJECT_ROOT\uv")) {
        New-Item -ItemType Directory -Path "$PROJECT_ROOT\uv" | Out-Null
    }
    
    # 下载并安装uv
    $uvInstaller = "$PROJECT_ROOT\uv\installer.ps1"
    try {
        Invoke-WebRequest -Uri "https://astral.sh/uv/install.ps1" -OutFile $uvInstaller
        & $uvInstaller --install-dir "$PROJECT_ROOT\uv"
        
        if (Test-Path "$PROJECT_ROOT\uv\uv.exe") {
            Write-Host "便携式uv安装成功！" -ForegroundColor Green
        } else {
            Write-Host "[ERROR] 便携式uv安装失败" -ForegroundColor Red
            exit 1
        }
    } catch {
        Write-Host "[ERROR] 下载uv安装器失败: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    } finally {
        if (Test-Path $uvInstaller) {
            Remove-Item -Force $uvInstaller
        }
    }
}

# 设置uv环境变量
$UV_EXE = "$PROJECT_ROOT\uv\uv.exe"
$env:PATH = "$PROJECT_ROOT\uv;$env:PATH"

# 创建虚拟环境
Write-Host "创建Python虚拟环境..." -ForegroundColor Cyan
if (-not (Test-Path "$PROJECT_ROOT\.venv")) {
    & $UV_EXE venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "虚拟环境创建成功！" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] 虚拟环境创建失败" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "虚拟环境已存在，跳过创建..." -ForegroundColor Yellow
}

# 配置清华源
Write-Host "配置清华源..." -ForegroundColor Cyan
& $UV_EXE pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
& $UV_EXE pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn

# 安装核心依赖
Write-Host "安装核心依赖..." -ForegroundColor Cyan
$coreDeps = @("PyQt5", "psutil", "pywin32", "pyinstaller", "pyyaml")
foreach ($dep in $coreDeps) {
    Write-Host "安装 $dep..." -ForegroundColor Yellow
    & $UV_EXE pip install $dep
}

# 安装开发依赖
Write-Host "安装开发依赖..." -ForegroundColor Cyan
$devDeps = @("opencv-python", "pillow", "pyautogui", "numpy")
foreach ($dep in $devDeps) {
    Write-Host "安装 $dep..." -ForegroundColor Yellow
    & $UV_EXE pip install $dep
}

Write-Host ""
Write-Host "环境设置完成！" -ForegroundColor Green
Write-Host "现在可以使用以下命令：" -ForegroundColor Cyan
Write-Host "  .\dev_run.ps1      - 运行程序" -ForegroundColor White
Write-Host "  .\dev_sync.ps1     - 同步依赖" -ForegroundColor White
Write-Host "  .\dev_build.ps1    - 打包exe" -ForegroundColor White
Write-Host ""
