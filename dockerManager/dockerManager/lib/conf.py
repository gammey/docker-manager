#!/usr/bin/python

#DockerList=[
#        {"name":"localhost","url":"http://192.168.1.203:2375/","version":"1.21"},
#        {"name":"swarm-docker-admin","url":"http://192.168.1.240:2375/","version":"1.26","role":"Master"},
#        {"name":"swarm-docker-node1","url":"http://192.168.1.241:2375/","version":"1.26"},
#        {"name":"swarm-docker-node2","url":"http://192.168.1.242:2375/","version":"1.26"}
#]
from loader import configLoad
from dockerManager.settings import dockerConfigFile
print("Using Config File:"+dockerConfigFile);
DockerList = configLoad(dockerConfigFile);


