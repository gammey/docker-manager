# docker-manager
功能：
用于管理多个docker节点的container，允许查看状态，以及简单启动关闭等操作。

演示：
源码git地址：https://github.com/gammey/docker-manager.git
演示地址：http://demo-docker.learn-learn.top/
演示图：



部署
1.安装docker服务

yum install docker -y
2.配置docker API接口
修改/etc/docker/daemon.json文件，并启动docker服务。

{
  "hosts": ["tcp://0.0.0.0:2375", "unix:///var/run/docker.sock"]
}
如果使用的是Centos6系统，请修改/etc/init.d/docker文件，将exec=”/usr/bin/$prog“改为：

exec="/usr/bin/$prog -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock"
3.查看docker接口版本：
记录下server端的API Version。若低于1.21版本，需要将docker的版本进行升级，可以按照文档(点击这里)进行操作。

[root@localhost ~]# docker version
Client:
 Version:      1.9.1
 API version:  1.21
 Go version:   go1.4.3
 Git commit:   a34a1d5
 Built:        Fri Nov 20 17:56:04 UTC 2015
 OS/Arch:      linux/amd64

Server:
 Version:      1.9.1
 API version:  1.21
 Go version:   go1.4.3
 Git commit:   a34a1d5
 Built:        Fri Nov 20 17:56:04 UTC 2015
 OS/Arch:      linux/amd64
4.下载代码

git clone https://github.com/gammey/docker-manager.git
5.简单配置

根据/dockerManager/dockerManager/下的docker.ini-sample创建docker.ini文件配置节点

例如：
[swarm-docker-admin]	#节点名称
name=swarm-docker-admin #节点名称
url=http://192.168.1.240:2375/  #docker API地址
version=1.26	#dockerAPI版本
role=Master	#如果是docker swarm mode的管理节点，设置成Master
6.进行发布

回到git的根目录执行bash install.sh;

7.访问

直接访问http://youripaddress:8001/即可。

说明：
由于这个这是测试版本，安全性尚未完善。所以请勿，发布到公网或重要业务系统。
