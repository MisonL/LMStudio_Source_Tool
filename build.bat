@echo off
chcp 65001 >nul
REM =======================================================
REM LM Studio换源工具 - 打包脚本 (兼容版)
REM 使用虚拟环境和固定版本PyInstaller打包
REM 解决"无法定位序数"错误
REM =======================================================

REM 设置变量
set VENV_NAME=build_venv
set OUTPUT_NAME=LMStudio_Source_Tool
set ERROR_OCCURRED=0
set PIP_INDEX_URL=--index-url https://mirrors.aliyun.com/pypi/simple/

echo =======================================================
echo LM Studio换源工具 - 打包脚本
echo =======================================================
echo.

REM 检查Python是否安装
echo [INFO] 正在检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] 未找到Python环境，请先安装Python 3.8或更高版本
    set ERROR_OCCURRED=1
    goto end
)
echo [OK] Python环境检查通过

REM 步骤1: 创建干净的虚拟环境
echo.
echo [STEP 1/6] 创建干净的虚拟环境: %VENV_NAME%
if exist %VENV_NAME% (
    echo [INFO] 删除已存在的虚拟环境...
    rd /s /q %VENV_NAME%
    if %errorlevel% neq 0 (
        echo [WARNING] 无法删除已存在的虚拟环境，可能正在使用中
    )
)
python -m venv %VENV_NAME%
if %errorlevel% neq 0 (
    echo [ERROR] 创建虚拟环境失败
    set ERROR_OCCURRED=1
    goto cleanup
)
echo [OK] 虚拟环境创建成功

REM 步骤2: 激活虚拟环境
echo.
echo [STEP 2/6] 激活虚拟环境
call %VENV_NAME%\Scripts\activate
if %errorlevel% neq 0 (
    echo [ERROR] 激活虚拟环境失败
    set ERROR_OCCURRED=1
    goto cleanup
)
echo [OK] 虚拟环境激活成功

REM 步骤3: 安装必要依赖
echo.
echo [STEP 3/6] 安装必要依赖
echo [INFO] 安装PyInstaller 5.12.0...
pip install pyinstaller==5.12.0 %PIP_INDEX_URL% --quiet
if %errorlevel% neq 0 (
    echo [ERROR] 安装PyInstaller失败
    set ERROR_OCCURRED=1
    goto cleanup
)

echo [INFO] 安装pywin32 306...
pip install pywin32==306 %PIP_INDEX_URL% --quiet
if %errorlevel% neq 0 (
    echo [ERROR] 安装pywin32失败
    set ERROR_OCCURRED=1
    goto cleanup
)

echo [INFO] 安装Pillow...
pip install pillow %PIP_INDEX_URL% --quiet
if %errorlevel% neq 0 (
    echo [ERROR] 安装Pillow失败
    set ERROR_OCCURRED=1
    goto cleanup
)
echo [OK] 依赖安装成功

REM 步骤4: 生成应用图标
echo.
echo [STEP 4/6] 生成应用图标
python create_icon.py
if %errorlevel% neq 0 (
    echo [ERROR] 生成图标失败
    set ERROR_OCCURRED=1
    goto cleanup
)
echo [OK] 图标生成成功

REM 步骤5: 打包应用程序
echo.
echo [STEP 5/6] 打包应用程序
echo [INFO] 开始打包，请稍候...
pyinstaller --onefile --windowed --icon=icons/app.ico --name "%OUTPUT_NAME%" --clean LMStudio_Source_Tool.py
if %errorlevel% neq 0 (
    echo [ERROR] 打包应用程序失败
    set ERROR_OCCURRED=1
    goto cleanup
)
echo [OK] 应用程序打包成功

echo.
echo [INFO] 打包完成！
echo [INFO] 可执行文件位置: dist\%OUTPUT_NAME%.exe

REM 步骤6: 清理虚拟环境
echo.
echo [STEP 6/6] 清理虚拟环境
goto cleanup

:cleanup
echo.
echo [CLEANUP] 清理资源...
deactivate >nul 2>&1
if exist %VENV_NAME% (
    rd /s /q %VENV_NAME%
    if %errorlevel% neq 0 (
        echo [WARNING] 无法删除虚拟环境目录，可能正在使用中
    ) else (
        echo [OK] 虚拟环境清理成功
    )
) else (
    echo [OK] 虚拟环境清理成功
)

if exist icons (
    rd /s /q icons
    if %errorlevel% equ 0 (
        echo [OK] 图标目录清理成功
    )
)

:end
echo.
echo =======================================================
if %ERROR_OCCURRED% equ 0 (
    echo 打包完成！所有步骤成功执行。
    echo 可执行文件位置: dist\%OUTPUT_NAME%.exe
) else (
    echo 打包过程中出现错误，请查看上面的日志信息。
)
echo =======================================================
echo.
echo 按任意键退出...
pause >nul