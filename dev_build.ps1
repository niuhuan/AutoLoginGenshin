# 原神自动登录工具 - 打包exe
# ============================

# 设置控制台编码为UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# 设置项目根目录
$PROJECT_ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $PROJECT_ROOT

Write-Host "原神自动登录工具 - 打包exe" -ForegroundColor Green
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

Write-Host "开始打包exe文件..." -ForegroundColor Cyan

# 检查PyInstaller是否安装
Write-Host "检查PyInstaller..." -ForegroundColor Yellow
try {
    & $UV_EXE pip show pyinstaller | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "PyInstaller not installed"
    }
} catch {
    Write-Host "安装PyInstaller..." -ForegroundColor Yellow
    & $UV_EXE pip install pyinstaller
}

# 清理之前的构建
Write-Host "清理之前的构建..." -ForegroundColor Yellow
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "*.spec") { Remove-Item -Force "*.spec" }

# 创建app.manifest文件
Write-Host "创建app.manifest..." -ForegroundColor Yellow
$manifestContent = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity version="1.0.0.0" processorArchitecture="*" name="AutoLoginGenshin" type="win32"/>
  <description>原神自动登录工具</description>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v2">
    <security>
      <requestedPrivileges xmlns="urn:schemas-microsoft-com:asm.v3">
        <requestedExecutionLevel level="requireAdministrator" uiAccess="false"/>
      </requestedPrivileges>
    </security>
  </trustInfo>
</assembly>
"@
$manifestContent | Out-File -FilePath "app.manifest" -Encoding UTF8

# 执行打包
Write-Host "执行PyInstaller打包..." -ForegroundColor Yellow
$pyinstallerArgs = @(
    "--onefile",
    "--name=AutoLoginGenshin",
    "--manifest=app.manifest",
    "--add-data=assets;assets",
    "--add-data=config.yaml;.",
    "--additional-hooks-dir=.",
    "--hidden-import=PyQt5",
    "--hidden-import=psutil",
    "--hidden-import=pywin32",
    "--hidden-import=win32gui",
    "--hidden-import=win32api",
    "--hidden-import=win32con",
    "--hidden-import=win32process",
    "--hidden-import=yaml",
    "--hidden-import=cv2",
    "--hidden-import=cv2.config",
    "--hidden-import=cv2.loader",
    "--hidden-import=numpy",
    "--hidden-import=PIL",
    "--hidden-import=pyautogui",
    "--collect-all=cv2",
    "--collect-all=numpy",
    "main.py"
)

& $UV_EXE run pyinstaller @pyinstallerArgs

if ($LASTEXITCODE -eq 0) {
    Write-Host "打包完成！exe文件位于 dist 目录" -ForegroundColor Green
    Write-Host "文件路径: $PROJECT_ROOT\dist\AutoLoginGenshin.exe" -ForegroundColor Cyan
} else {
    Write-Host "打包失败！" -ForegroundColor Red
    exit 1
}

# 清理临时文件
Write-Host "清理临时文件..." -ForegroundColor Yellow
if (Test-Path "app.manifest") { Remove-Item -Force "app.manifest" }
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "*.spec") { Remove-Item -Force "*.spec" }

Write-Host "打包流程完成！" -ForegroundColor Green
