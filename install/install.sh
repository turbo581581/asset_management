#!/bin/bash

##python3
sudo apt-get update
sudo apt-get install python-pip python3-pip python3-dev python3-tk
sudo pip3 install --upgrade pip

pip install -Ur requirements.txt

set -e  # 任何命令失败则退出，可按需关闭

packages=("zip" "curl" "wget" "git" "htop")

install_if_missing() {
    local pkg="$1"

    # 检查是否安装
    if dpkg -s "$pkg" >/dev/null 2>&1; then
        echo "✔ $pkg is already installed."
        return
    fi

    echo "➜ $pkg not found. Installing..."

    # 仅首次更新 apt 缓存
    if [ "$APT_UPDATED" != "1" ]; then
        echo "Updating apt package list..."
        sudo apt-get update -y
        APT_UPDATED=1
    fi

    # 安装
    if sudo apt-get install -y "$pkg"; then
        echo "✔ $pkg installed successfully."
    else
        echo "✘ Failed to install $pkg." >&2
        exit 1
    fi
}

# 遍历安装
for pkg in "${packages[@]}"; do
    install_if_missing "$pkg"
done