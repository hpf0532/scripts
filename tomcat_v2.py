#!/root/scripts/venv/bin/python
#coding=utf8
from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
from fabric.contrib.console import confirm
import sys
import time
import os
import hashlib
import re

env.user='root'
env.hosts=['192.168.1.161']
env.local_path='/root/project/'
env.remote_base_path='/root/project'
env.remote_dir='/opt/tomcat'
env.dir_dict={'backend':'webapps_bd', 'h5pay':'webapps_h5_pay', 'posmerchant':'webapps_pos'}

pack = raw_input('请输入包名: ').strip()
print pack
pg_prefix = pack.split('.')[0]
now = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))
red_war = '%s_%s.war' % (pg_prefix, now)
app_dir = '%s/%s' % (env.remote_dir, env.dir_dict[pg_prefix])
remote_dir = '%s/%s/' % (env.remote_base_path, pg_prefix)


@task
def put_package():
    print(yellow('重命名war包！'))
    with lcd(env.local_path):
        command = "ls -l | grep %s$" % pack
        result = local(command, capture=True)
        local('mv %s %s_%s.war' % (pack, pg_prefix, now))
        print remote_dir
        command = '[ ! -e %s ] && mkdir -p %s || /bin/true' % (remote_dir, remote_dir)
        run(command)
        print(yellow('开始上传。。。'))
        time.sleep(3)
        put(red_war, remote_dir)

@task
def roll_back():
    print(yellow('回滚版本！'))
    with cd(remote_dir):
        global rollback_ver
        rollback_ver = run("ls -l last_version | awk '{print $NF}'")
        print 'name:', rollback_ver

@task
def backup():
    print(yellow('备份...'))
    with cd(app_dir):
        rootmd5 = run('md5sum %s' % 'ROOT.war').split(' ')[0]
        print '====================================================='
    with cd(remote_dir):
        print 'rootmd5', rootmd5
        a = run("for I in $(ls -l | awk 'NR!=1{print $NF}'); do md5sum $I ; done")
        print a
        if rootmd5  in a:
            print 'YES' 
            last_ver_list = re.findall(r'%s.*war' % rootmd5, a)
            print last_ver_list
            last_ver = last_ver_list[0]
            b = last_ver.split('  ')[1]
            run('[ -e last_version ] && rm -f last_version || /bin/true')
            run('ln -sv %s last_version' % b)
        else:
            print 'NO'
            sys.exit('没有备份')

@task
def pack_validate():
    print app_dir
    print(yellow('比对文件md5值：'))
    lmd5 = local('md5sum %s%s' % (env.local_path, red_war), capture=True).split(' ')[0]
    rmd5 = run('md5sum %s/%s/%s' % (env.remote_base_path, pg_prefix, red_war)).split(' ')[0]
    print 'remote' + '     ' + rmd5
    print 'local' + '    ' + lmd5
    if lmd5 == rmd5:
        print(yellow('比对成功！开始部署。。。'))
    else:
        print(red('文件上传错误，请重试！'))
        sys.exit()

@task
def deploy(war):
    with cd(app_dir):
        run('rm -rf ROOT*')
        root_war = '%s%s' %(remote_dir, war)
        print root_war
        run('cp %s ./ROOT.war' % root_war) 
    print(yellow('部署成功！准备重启服务。。。'))

@task
def restart_serv():
    print(red('重启tomcat!'))
    with settings(warn_only=True):
        result = run('set -m;/etc/init.d/tomcat stop')
#        result = run('set -m;/opt/tomcat/bin/shutdown.sh')
    if result.failed and not confirm('Command failed.Continue anyway?'):
        abort('Aborting at user request.')
    time.sleep(3)
    run('set -m;/etc/init.d/tomcat start')

@task
def production():
    backup()
    put_package()
    pack_validate()
    deploy(red_war)
    restart_serv()

@task
def rollback():
    roll_back()
    backup()
    deploy(rollback_ver)
    restart_serv()
