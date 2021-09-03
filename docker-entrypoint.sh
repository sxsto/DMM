#!/bin/bash
set -e

dir_shell=/ql/shell
. $dir_shell/share.sh
link_shell
echo -e "======================1. 检测配置文件========================\n"
fix_config
cp -fv $dir_root/docker/front.conf /etc/nginx/conf.d/front.conf
pm2 l >/dev/null 2>&1
echo

echo -e "======================2. 安装依赖========================\n"
update_depend
echo

echo -e "======================3. 启动nginx========================\n"
nginx -s reload 2>/dev/null || nginx -c /etc/nginx/nginx.conf
echo -e "nginx启动成功...\n"

echo -e "======================4. 启动控制面板========================\n"
if [[ $(pm2 info panel 2>/dev/null) ]]; then
  pm2 reload panel --source-map-support --time
else
  pm2 start $dir_root/build/app.js -n panel --source-map-support --time
fi
echo -e "控制面板启动成功...\n"

echo -e "======================5. 启动定时任务========================\n"
if [[ $(pm2 info schedule 2>/dev/null) ]]; then
  pm2 reload schedule --source-map-support --time
else
  pm2 start $dir_root/build/schedule.js -n schedule --source-map-support --time
fi
echo -e "定时任务启动成功...\n"

if [[ $AutoStartBot == true ]]; then
  echo -e "======================6. 启动bot========================\n"
  nohup ql bot >>$dir_log/start.log 2>&1 &
  echo -e "bot后台启动中...\n"
fi

if [[ $EnableExtraShell == true ]]; then
  echo -e "======================7. 执行自定义脚本========================\n"
  nohup ql extra >>$dir_log/start.log 2>&1 &
  echo -e "自定义脚本后台执行中...\n"
fi

DMM_WORKDIR=/ql/dmm
DMM_REPO_URL=https://ghproxy.com/https://github.com/sxsto/dmm

# clone dmm仓库，环境变量 DMM_REPO_URL
if [[ ! -f "$DMM_WORKDIR/dmm" ]]; then
  echo -e "=================== 未检测到大咪咪可执行文件，开始编译大咪咪 ==================="
  cd /ql
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
echo -e "容器启动成功..."
echo -e "\n请先访问5700端口，登录成功面板之后再执行添加定时任务..."
echo -e "############################################################\n"

crond -f >/dev/null

exec "$@"