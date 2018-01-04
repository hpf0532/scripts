# coding=utf-8
import multiprocessing
import os
import time
import subprocess


print time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime(time.time()))

def sayHi(name):
    cmd =  'rsync -avzL /mnt/wwwroot/cashloan/public/attachment/%s  hpf@192.168.1.11::attachment --password-file=/etc/rsyncd.password' % name
    subprocess.call(cmd, shell=True)
    print 'end'

pool = multiprocessing.Pool(processes = 7)

for i in [d for d in os.listdir('/mnt/wwwroot/cashloan/public/attachment/')]:
    pool.apply_async(sayHi, (i, ))

pool.close()
pool.join()

print time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime(time.time()))
