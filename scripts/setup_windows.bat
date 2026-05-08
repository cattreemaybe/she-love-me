@echo off
chcp 65001 >nul 2>&1
title 她不一样 · 一键启动

echo.
echo ╔══════════════════════════════════════════════╗
echo ║         她不一样 · 一键启动工具              ║
echo ╚══════════════════════════════════════════════╝
echo.

:: 检查是否以管理员身份运行
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] 需要管理员权限运行此脚本。
    echo.
    echo     请右键点击此文件，选择「以管理员身份运行」
    echo.
    pause
    exit /b 1
)

:: ── 检查 Python ──
where python >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] 未检测到 Python。
    echo.
    echo     正在打开 Python 下载页面...
    echo     下载后安装时，请务必勾选底部的「Add Python to PATH」
    echo     安装完成后，重新运行此脚本。
    echo.
    start https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [*] Python:
python --version
echo.

:: ── 检查项目文件 ──
if exist "scripts\one_click.py" (
    echo [*] 项目文件已就绪
    goto :run
)

:: 项目文件不存在，尝试自动获取
echo [*] 未找到项目文件，尝试自动下载...
echo.

:: 优先用 git clone
where git >nul 2>&1
if %errorLevel% equ 0 (
    echo [*] 检测到 Git，正在 clone 项目...
    echo.
    git clone https://github.com/863401402/she-love-me.git
    if %errorLevel% equ 0 (
        cd she-love-me
        goto :run
    )
    echo [!] Git clone 失败，尝试 zip 下载...
    echo.
)

:: 没有 git 或 clone 失败，用 PowerShell 下载 zip
echo [*] 正在下载项目 zip...
echo.

powershell -Command "& {$ProgressPreference='SilentlyContinue'; Invoke-WebRequest -Uri 'https://github.com/863401402/she-love-me/archive/refs/heads/main.zip' -OutFile 'she-love-me.zip'}"

if not exist "she-love-me.zip" (
    echo [!] 下载失败。请检查网络连接。
    echo.
    echo     或者手动操作：
    echo     1. 安装 Git: https://git-scm.com/download/win
    echo     2. 打开终端执行: git clone https://github.com/863401402/she-love-me.git
    echo     3. 进入目录重新运行此脚本
    echo.
    pause
    exit /b 1
)

echo [*] 解压中...
powershell -Command "Expand-Archive -Path 'she-love-me.zip' -DestinationPath '.' -Force"
del she-love-me.zip

if exist "she-love-me-main" (
    cd she-love-me-main
    goto :run
)

echo [!] 解压异常，请手动解压 she-love-me.zip
pause
exit /b 1

:run
echo.
echo ══════════════════════════════════════════════
echo   项目就绪，启动分析工具...
echo ══════════════════════════════════════════════
echo.

python scripts\one_click.py

echo.
echo [*] 程序已结束。
pause
