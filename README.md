<h1 align="center">LM Studio 源管理工具</h1>

<p align="center">
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.8%2B-blue" alt="Python"></a>
  <a href="https://www.microsoft.com/windows"><img src="https://img.shields.io/badge/Platform-Windows-lightgrey" alt="Platform"></a>
</p>

## 简介

LM Studio 源管理工具是一个用于替换 LM Studio 中 huggingface.co 域名为 hf-mirror.com 的工具，以提高在中国大陆地区的下载速度。

该工具提供图形用户界面，使用户能够轻松地一键更换源地址，从而显著提升模型下载速度。

## 功能特点

- 🖥️ **图形用户界面** - 操作简单直观
- 🔍 **自动路径检测** - 自动检测 LM Studio 安装路径
- ⚡ **一键换源功能** - 自动备份、替换、验证
- 🔄 **还原备份功能** - 一键恢复原始文件
- 📂 **自定义路径支持** - 支持手动选择安装路径
- 📝 **详细日志记录** - 完整的操作过程记录
- 🛡️ **权限管理** - 自动请求管理员权限

## 使用方法

### 快速开始

1. 下载并解压发行版文件
2. 双击运行 `LMStudio_Source_Tool.exe`
3. 程序会自动请求管理员权限
4. 在图形界面中：
   - 自动检测安装路径或手动浏览选择
   - 点击"一键换源"执行全流程
   - 或使用"还原备份"恢复原始文件

### 详细步骤

1. **启动程序**
   - 双击 `LMStudio_Source_Tool.exe`
   - 程序会自动请求管理员权限以修改系统文件

2. **路径检测**
   - 程序会自动检测 LM Studio 安装路径
   - 如果自动检测失败，可以手动浏览选择安装目录

3. **执行换源**
   - 点击"一键换源"按钮
   - 程序会自动：
     * 创建原始文件备份 (.bak)
     * 替换 huggingface.co 为 hf-mirror.com
     * 验证替换结果

4. **还原备份**
   - 如需恢复原始文件，点击"还原备份"按钮
   - 程序会从 .bak 文件恢复原始内容

## 编译和打包

### 环境要求

- Python 3.8 或更高版本
- Windows 10/11 操作系统
- 管理员权限

### 编译步骤

1. **克隆仓库**
   ```bash
   git clone <repository-url>
   cd lm-studio-source-tool
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```
   
   或单独安装：
   ```bash
   pip install pyinstaller==5.13.0
   pip install pywin32==306
   pip install pillow
   ```

3. **生成图标**
   ```bash
   python create_icon.py
   ```

4. **编译为可执行文件**
   ```bash
   pyinstaller --onefile --windowed --icon=icons/app.ico --name "LMStudio_Source_Tool" --clean LMStudio_Source_Tool.py
   ```

### 打包发行版

使用提供的打包脚本：

1. **Windows 批处理脚本**
   ```bash
   .\build.bat
   ```

2. **Python 打包脚本**
   ```bash
   python build_release.py
   ```

3. **输出文件**
   - 可执行文件：`dist\LMStudio_Source_Tool.exe`
   - 发行版：`release\LMStudio_Source_Tool_vX.X.X.zip`

### 作者

- **姓名**: Mison
- **邮箱**: 1360962086@qq.com

### 技术栈

- **主要语言**: Python 3.10
- **GUI 框架**: Tkinter
- **打包工具**: PyInstaller 5.12.0
- **图标处理**: Pillow

### 项目结构
```
lm-studio-source-tool/
├── LMStudio_Source_Tool.py     # 主程序源代码
├── build.bat                   # Windows 打包脚本
├── build_release.bat           # 发行版构建脚本
├── create_icon.py              # 图标生成脚本
├── requirements.txt            # 依赖列表
├── README.md                  # 项目说明文档
├── LICENSE                    # 许可证文件
├── .gitignore                 # Git 忽略文件
├── dist/                      # 编译输出目录
├── release/                   # 发行版目录
└── icons/                     # 图标资源目录
```

### 运行开发版本

要运行开发版本而不打包为可执行文件：

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 运行主程序：
   ```bash
   python LMStudio_Source_Tool.py
   ```

## 版本历史

### v2.0 (2025-07-26)
- 重构为图形界面版本
- 添加自动路径检测功能
- 改进错误处理和日志记录
- 添加版本信息和图标
- 增强用户界面交互

### v1.x
- 批处理脚本版本
- 基本的换源和还原功能

## 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。

```
MIT License

Copyright (c) 2025 Mison

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 贡献指南

欢迎任何形式的贡献！

### 报告问题
- 使用 GitHub Issues 报告 bug
- 详细描述问题现象和重现步骤
- 提供系统环境信息（Windows 版本、Python 版本等）

### 提交代码
1. Fork 项目仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 开发规范
- 遵循 PEP 8 Python 编码规范
- 添加适当的注释和文档
- 确保代码兼容 Python 3.8+

## 常见问题

### 1. 程序无法启动
- 确保以管理员权限运行
- 检查杀毒软件是否阻止程序执行
- 确认 LM Studio 已正确安装

### 2. 换源失败
- 检查 LM Studio 安装路径是否正确
- 确认目标文件存在且可写
- 查看日志信息获取详细错误说明

### 3. 还原备份失败
- 检查备份文件 (.bak) 是否存在
- 确认文件权限是否正确
- 查看日志信息获取详细错误说明

### 4. 打包过程中出现"无法定位序数"错误
- 这是由于动态链接库兼容性问题导致的
- 解决方案：
  * 使用 `build.bat` 脚本自动处理依赖
  * 确保使用 Python 3.8+ 版本
  * 脚本会自动创建虚拟环境并安装兼容版本的依赖包

## 致谢

- 感谢 [hf-mirror.com](https://hf-mirror.com) 提供的镜像服务
- 感谢 [PyInstaller](https://www.pyinstaller.org/) 项目
- 感谢所有开源组件的贡献者

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/Mison">Mison</a>
</p>