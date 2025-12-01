# asset_management

资产管理与经济建模相关脚本的集中仓库。当前项目聚焦于整理常用的实验脚本、安装配置流程以及开发中高频使用的命令，便于在新环境中快速复用。

## 目录结构

```
├── install/                 # 环境安装脚本与 Python 依赖列表
├── develop_command/         # 常用命令速查表（CMake、Docker、GDB 等）
├── script/
│   ├── investment_game/     # 投资博弈相关脚本与实验草稿（可自行补充）
│   └── micro_economic/      # 微观经济专题脚本（占位目录）
└── README.md
```

## 快速开始

1. **安装系统依赖与 Python 包**
   ```bash
   cd install
   bash install.sh
   ```
   - 脚本会安装常用工具（zip/curl/wget/git/htop）以及 `install/requirements.txt` 中列出的 Python 包。
   - 若不方便使用 `sudo`，可以手动参考脚本内容逐条执行。

2. **激活 Python 环境（可选）**
   建议使用 virtualenv/conda，避免污染系统环境。创建完成后再次执行 `pip install -Ur requirements.txt`。

3. **编写/运行脚本**
   - 将自己的研究脚本放入 `script/investment_game` 或 `script/micro_economic` 中。
   - 若脚本带有可执行权限，推荐在文件头声明解释器：`#!/usr/bin/env python3`。

## 常用命令速查

`develop_command/common_command.sh` 汇总了构建、调试、Docker、批量授权等高频命令，可直接复制粘贴使用。例如：
- CMake 构建：`cmake -B build -S . ...`
- Core dump 与 GDB 调试的快速配置。
- Docker 镜像构建、推送与常见加速配置。

## 贡献指南

1. 以功能模块为单位在 `script/` 下新增子目录。
2. README 中同步更新目录说明，让团队成员可以快速理解每个脚本的定位。
3. 需要新依赖时更新 `install/requirements.txt`，必要时补充安装说明。

如有新的工具或命令，也欢迎追加到 `develop_command/common_command.sh`，保持仓库在新机器上“开箱即用”。***
