#!/bin/bash
set -e

DMM_WORKDIR=/root/dmm
DMM_REPO_URL=https://ghproxy.com/https://github.com/sxsto/dmm

# clone dmm仓库，环境变量 DMM_REPO_URL
if [[ ! -f "$DMM_WORKDIR/dmm" ]]; then
  echo -e "=================== 未检测到大咪咪可执行文件，开始编译大咪咪 ==================="
  cd /root
  git clone "$DMM_REPO_URL" $DMM_WORKDIR
  cd $DMM_WORKDIR
  go build
  chmod 777 dmm
  echo -e "=================== 大咪咪编译完毕 ==================="
fi

# 启动dmm
echo -e "=================== 启动大咪咪（第一次可能启动较慢） ==================="
echo -e "=================== 如果需要配置QQ机器人，请手动以前台模式启动 ==================="
cd "$DMM_WORKDIR" && ./dmm -d

echo -e "############################################################\n"
echo -e "大咪咪启动成功..."
echo -e "\n请访问5701端口，登录管理后台..."
echo -e "############################################################\n"

# crond -f >/dev/null

exec "$@"