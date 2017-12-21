#!/bin/bash
REDIS_VER=4.0.6
TOOLS_DIR=/root/soft/
INSTALL_DIR=/usr/local

# Check if user is root
if [ $(id -u) != "0" ]; then
    echo "Error: You must be root to run this script"
    exit 1
fi
# Check network environmental
NET_NUM=`ping -c 4 www.baidu.com |awk '/packet loss/{print $6}' |sed -e 's/%//'`
#NET_NUM=`ping -c 4 www.baidu.com |awk '/packet loss/{print $6}'`
if [ -z "$NET_NUM" ] || [ $NET_NUM -ge 10 ];then
        echo "Please check your internet"
        exit 1
fi

[ ! -d $TOOLS_DIR ] && mkdir -pv $TOOLS_DIR 
cd $TOOLS_DIR

if [ ! -f redis-${REDIS_VER}.tar.gz ]; then
    wget http://download.redis.io/releases/redis-${REDIS_VER}.tar.gz
fi
tar xf redis-${REDIS_VER}.tar.gz -C $INSTALL_DIR
cd $INSTALL_DIR
[ ! -e $INSTALL_DIR/redis ] && ln -sv $INSTALL_DIR/redis-${REDIS_VER} $INSTALL_DIR/redis

#Compile redis
cd $INSTALL_DIR/redis
make

make PREFIX=/usr/local/redis install

[ ! -d etc ] && mkdir etc 
\cp -f redis.conf etc/
sed  -i 's#daemonize no#daemonize yes#g' etc/redis.conf

#Start redis-server
${INSTALL_DIR}/redis/bin/redis-server ${INSTALL_DIR}/redis/etc/redis.conf

#auto start
if [ `grep redis-server /etc/rc.d/rc.local | wc -l` -eq 0 ]; then
    echo "${INSTALL_DIR}/redis/bin/redis-server ${INSTALL_DIR}/redis/etc/redis.conf &>/dev/null" >> /etc/rc.d/rc.local
fi
