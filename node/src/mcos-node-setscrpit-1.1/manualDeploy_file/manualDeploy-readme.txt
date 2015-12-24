1.设置IP地址。

2.设置/etc/hosts/及/etc/hostname文件
注：在修改hosts时需要添加的格式为：
192.168.15.131 master.server.com

192.168.15.131 node1 node1.localdomain

3.修改/etc/openstack.cfg及/etc/openstack_deploy.conf文件

4.删除/etc/yum.repos.d/cobbler-config.repo文件

5.执行python /usr/local/bin/manualDeployment.py


