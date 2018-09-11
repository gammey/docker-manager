#!/usr/bin/python
import docker
import json
import conf

dockerlist = conf.DockerList

#lient = docker.DockerClient(DockerList[0]["url"],DockerList[0]["version"]);
#rint client.containers.list(all=True)

class dockerNode:
	def __init__(self,url,version):
		self.url = url;
		self.version = version;
		self.client = docker.DockerClient(self.url,self.version);
	def list(self):
		return self.client.containers.list(all=True);
	def listSimple(self,status="all"):
		reList=[];
		for i in self.list():
			a={};
			a['sid']=i.short_id;
			a['name']=i.name;
			a['status']=i.status;
			a['image']=i.attrs['Config']['Image'];
			if status != "all":
				if i.status == status:
					reList.append(a);
			else:
				reList.append(a);
		return reList;
	def searchContainer(self,name):
		try:
			return self.client.containers.get(name);
		except:
			return 0;
	def getContainerNetworkSettings(self,name):
		container = self.searchContainer(name);
		if container == 0:
			return 0;
		else:
			redict={};
			redict['IPAddress']=container.attrs['NetworkSettings']['IPAddress'];
			redict['Gateway']=container.attrs['NetworkSettings']['Gateway'];
			return redict;
	def getContainerDetail(self,name):
		container = self.searchContainer(name);
                if container == 0:
                        return 0;
                else:
                        return container.attrs;
	def getContainerFullDetail(self,name):
		redict = {};
		container = self.searchContainer(name);
                if container == 0:
                        return 0;
                else:   
                        redict["detail"] = container.attrs;
			redict["stats"] = container.stats(decode=True,stream=False);
			return redict;
	def getContainerExposePorts(self,name):
		container = self.searchContainer(name);
                if container == 0:
                        return 0;
                else:
                        portsList = container.attrs['Config']['ExposedPorts'].keys();			
			reList=[];	
			for i in portsList:
				postcfg = container.attrs['NetworkSettings']['Ports'][i][0];
				hostpost = postcfg['HostIp']+":"+postcfg['HostPort'];
				reList.append({i:hostpost});
			return reList;
	def listServices(self):
		reList = [];
		servicelist = self.client.services.list();
		for i in servicelist:
			reList.append(i.attrs);
		return reList;
	def listContainerSimple(self,status="all"):
		reList=[];
		for i in self.listContainers():
			a={};
			a['sid']=i.short_id;
			a['name']=i.name;
			a['status']=i.status;
			a['image']=i.attrs['Config']['Image'];
			if status != "all":
				if i.status == status:
					reList.append(a);
			else:
				reList.append(a);
		return reList;
	def listContainers(self):
		return self.client.containers.list(all=True);
	def allContainerDetails(self):
                nodelist = self.listContainerSimple();
                relist = [];
                for i in nodelist:
                        redict = {}
                        redict["name"] = i["name"];
                        redict["detail"] = self.getContainerDetail(i["name"]);
                        node = self.searchContainer(i["name"])
                        redict["stats"] = node.stats(decode=True,stream=False);
                        relist.append(redict);
                return relist;
	def listImages(self):
		relist = [];
		ilist = self.client.images.list();
		for i in ilist:
			detail = i.attrs;
			relist.append(detail);
		return relist;
	def delImage(self,name):
		try: 
			im = self.client.images.get(name);
		except:
			return "Image not exsit";
		try:
			self.client.images.remove(name);
			return 0;
		except:
			return "Remove Image Failed.";
	def historyImage(self,name):
		try:
                        im = self.client.images.get(name);
                except:
                        return "Error";
                try:
                        return self.client.images.get(name).history();
                except:
                        return "Error";
	def startContainer(self,name):
		container = self.searchContainer(name);
		if container != 0: 
			container.start();
		else:
			return 0;
	def stopContainer(self,name):
		container = self.searchContainer(name);
		if container != 0:
                        container.stop();
                else:
                        return 0;
	def restartContainer(self,name):
		container = self.searchContainer(name);
		if container != 0:
                        container.restart();
                else:
                        return 0;
	def removeContainer(self,name):
		container = self.searchContainer(name);
		if container != 0:
                        container.remove();
                else:
                        return 0;

def searchNode(nodelist,nodename):
        for i in nodelist:
                if i["name"] == nodename:
                        return dockerNode(i["url"],i["version"]);
	return 0;
