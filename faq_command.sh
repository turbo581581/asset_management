#common commands
mkdir build && cd build
cmake -DGFLAGS_NAMESPACE=google -DCMAKE_CXX_FLAGS=-fPIC -DBUILD_SHARED_LIBS=ON ..
make
sudo make install

#file size
du -h --max-depth=1
df -h
mount /dev/sda /mnt/ssd

#批量更改目录下所有文件的后缀名
find  $PWD | xargs rename 's/\.hpp/\.h/'
find  $PWD | xargs rename 's/\.cpp/\.cc/'
find . -name "libglog.so*"

#视频截取命令
ffmpeg -ss 00:00:05 -t 00:00:10 -i input.mp4 -c copy output.mp4

#find link in lib.so
nm  ./lib/libboost_context.so.1.65.0 |c++filt |grep ontop_fcontext

#docker
docker login https://adas-img.nioint.com/harbor/
docker search turbo --filter=STARS=100
docker pull turbo581
docker image ls -al
docker build -t ubuntu .
docker container ls -al
docker run -it -v ~/docker:/workspace turbo581/2 /bin/bash
docker commit fb7a9d9b558f mapoffset_v1.3
docker tag mapoffset_v1.3:latest adas-img.nioint.com/localization/mapoffset:1.3
docker push adas-img.nioint.com/localization/mapoffset:1.3
sudo vim /etc/docker/daemon.json
{
 "registry-mirrors": ["https://registry.docker-cn.com","https://nrbewqda.mir    ror.aliyuncs.com","https://dmmxhzvq.mirror.aliyuncs.com"]
}

#gdb https://www.cnblogs.com/hazir/p/linxu_core_dump.html
ulimit -a
ulimit -c unlimited
cmakelists add_definitions("-Wall -ggdb")
echo "/tmp/corefile-%e-%p-%t" > /proc/sys/kernel/core_pattern
gdb -q -ex=r --args
r args -l a -C abc
bt

##cpu mem[pid, VIRT, cpu, mem, command]
top -b -n 1 | sed 's/ //' | sed 's/[ ][ ]*/,/g' | grep rviz

##give rights to all files
sudo chmod 777 -R *

