#!/bin/bash
arch=`uname -m`
case $arch in
x86_64)
     arch="amd64"
     ;;
aarch64)
     arch="arm64"
     ;;
*)
     arch="arm"
     ;;
esac
filename="dmm_linux_${arch}"
url="https://ghproxy.com/https://github.com/sxsto/dmm/releases/download/main/${filename}"
dirname="dmm"
cd $HOME
if [ ! -d dirname ];then
  mkdir dirname
fi
cd dmm
curl -L $url -O $filename
