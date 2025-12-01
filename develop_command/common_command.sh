1) 🏗️ CMake / Build 常用指令（更稳健）
一键构建（自动建目录）
cmake -B build -S . \
  -DGFLAGS_NAMESPACE=google \
  -DCMAKE_CXX_FLAGS="-fPIC" \
  -DBUILD_SHARED_LIBS=ON

cmake --build build -j$(nproc)
sudo cmake --install build

优点：
-B -S 不需要 cd
自动使用 CPU 核数
更适合写脚本

2) 📦 文件大小 / 磁盘 / 挂载
查看文件夹大小（更短）
du -h --max-depth=1 .

查看磁盘盘符
df -hT

挂载 SSD（先创建挂载点）
sudo mkdir -p /mnt/ssd
sudo mount /dev/sda /mnt/ssd

3) 📝 批量修改后缀名（更安全 + 更精确）

你的版本有风险（find $PWD | xargs rename 会误伤目录）。

更安全版（仅匹配文件）
find . -type f -name "*.hpp" -exec rename 's/\.hpp$/.h/' {} +
find . -type f -name "*.cpp" -exec rename 's/\.cpp$/.cc/' {} +

查找某个库
find . -name "libglog.so*"

4) 🎬 视频截取（最短 + 精确）

ffmpeg -ss 5 -t 10 -i input.mp4 -c copy output.mp4

5) 🔍 查找符号（nm + demangle）
nm -D ./lib/libboost_context.so.1.65.0 | c++filt | grep ontop_fcontext

加 -D 只看动态符号，输出更干净。

6) 🐳 Docker 最佳速查指令（Turbo版）
Login
docker login adas-img.nioint.com/harbor/

搜索镜像（带过滤）
docker search turbo --filter stars=100

本地镜像列表 (按大小排序)
docker image ls --digests --format "table {{.Size}}\t{{.Repository}}:{{.Tag}}" | sort -h

构建镜像
docker build -t ubuntu .

启动容器
docker run -it -v ~/docker:/workspace turbo581/2 bash

快速打包容器为镜像
docker commit <container_id> mapoffset:v1.3

给镜像打标签 & 推送
docker tag mapoffset:v1.3 adas-img.nioint.com/localization/mapoffset:1.3
docker push adas-img.nioint.com/localization/mapoffset:1.3

Docker 加速（daemon.json）
{
  "registry-mirrors": [
    "https://registry.docker-cn.com",
    "https://nrbewqda.mirror.aliyuncs.com",
    "https://dmmxhzvq.mirror.aliyuncs.com"
  ]
}

7) 🐞 GDB / Core dump 调试（专业最简）
开启 core dump
ulimit -c unlimited
echo "/tmp/core-%e-%p-%t" | sudo tee /proc/sys/kernel/core_pattern

CMake 开启调试
add_definitions(-Wall -ggdb)

GDB 运行
gdb -q --args ./app -l a -C abc
run
bt

8) 📊 CPU / 内存 / 进程过滤（超简写法）

原命令很多 sed 太重，这里给你更快的：

查看 rviz 进程
ps aux | grep rviz

或者更漂亮的
ps -eo pid,pcpu,pmem,cmd --sort=-pcpu | grep rviz
输出格式：PID、CPU%、MEM%、命令

9) 🔐 批量授权（安全写法）

你原来的写法：
sudo chmod 777 -R *

改成最安全合理版（775）
sudo chmod -R u+rwX,g+rwX,o+rX .

如果你确实需要 777（建议只在某些目录）
sudo find . -type d -exec chmod 777 {} +
sudo find . -type f -exec chmod 666 {} +