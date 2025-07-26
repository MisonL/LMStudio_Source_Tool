@echo off
chcp 65001
REM =======================================================
REM LM Studio换源工具 - 发布包构建脚本
REM =======================================================

echo 步骤1: 清理旧的发布目录
if exist release rd /s /q release

echo 步骤2: 创建发布目录结构
mkdir release
mkdir release\icons

echo 步骤2.1: 生成图标文件
python create_icon.py

echo 步骤2.2: 复制图标文件
copy icons\app.ico release\icons\icon.ico

echo 步骤3: 复制可执行文件
copy "dist\LMStudio_Source_Tool.exe" "release\LMStudio_Source_Tool.exe"

echo 步骤4: 复制文档
copy "README.md" "release\README.md"

echo 步骤5: 创建版本信息文件
echo LM Studio 源管理工具 v2.0 > release\VERSION.txt
echo. >> release\VERSION.txt
echo 发布日期: %date% >> release\VERSION.txt
echo 发布时间: %time% >> release\VERSION.txt

echo 步骤6: 创建使用说明
echo ======================================================= > release\使用说明.txt
echo           LM Studio 源管理工具 v2.0                   >> release\使用说明.txt
echo ======================================================= >> release\使用说明.txt
echo. >> release\使用说明.txt
echo 使用方法: >> release\使用说明.txt
echo 1. 双击运行 LMStudio_Source_Tool.exe >> release\使用说明.txt
echo 2. 程序会自动请求管理员权限 >> release\使用说明.txt
echo 3. 在图形界面中: >> release\使用说明.txt
echo    - 自动检测安装路径或手动浏览选择 >> release\使用说明.txt
echo    - 点击"一键换源"执行全流程 >> release\使用说明.txt
echo    - 或使用"还原备份"恢复原始文件 >> release\使用说明.txt
echo. >> release\使用说明.txt
echo 注意事项: >> release\使用说明.txt
echo - 运行程序需要管理员权限 >> release\使用说明.txt
echo - 程序会自动备份原始文件 >> release\使用说明.txt
echo - 如需恢复，使用"还原备份"功能 >> release\使用说明.txt
echo. >> release\使用说明.txt
echo 开发者信息: >> release\使用说明.txt
echo 作者: Mison >> release\使用说明.txt
echo 邮箱: 1360962086@qq.com >> release\使用说明.txt
echo 许可证: MIT >> release\使用说明.txt
echo ======================================================= >> release\使用说明.txt

echo.
echo =======================================================
echo 发布包构建完成！
echo 发布文件位置: release\
echo 包含文件:
echo   - LMStudio_Source_Tool.exe (主程序)
echo   - README.md (详细说明)
echo   - VERSION.txt (版本信息)
echo   - 使用说明.txt (简要使用指南)
echo =======================================================