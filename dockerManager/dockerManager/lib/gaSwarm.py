#!/usr/bin/python
import docker
import json
import gaDocker
import conf

class gaSwarm:
	def __init__(self,url,version,confList):
		self.url = url;
		self.version = version;
		self.confList = confList;
		self.client = docker.DockerClient(self.url,self.version);
	def nodeClientList(self):
		reList = [];
		try:
			nodelist = self.client.nodes.list();
		except AttributeError:
			nodelist = self.client.nodes();
		except docker.errors.APIError:
			print("Client is not Swarm Master,");
			return 0;
		for i in nodelist:
			try:
				nodeAddr = i.attrs['Status']['Addr'];
			except:
				nodeAddr = i['Status']['Addr'];
			if nodeAddr == "127.0.0.1":
				for i in self.confList:
					if i["name"] == "localhost":
						client = docker.DockerClient(i["url"],i["version"]);
                                       		redict = {"name":i["name"],"client":client}
                                        	reList.append(redict);
						break;
			else:
				for i in self.confList:
					if nodeAddr == i["url"].split("/")[2].split(":")[0]:
						client = docker.DockerClient(i["url"],i["version"]);
						redict = {"name":i["name"],"client":client}
						reList.append(redict);
						break;
		return reList;
	def containerList(self):
		reList = [];
		for i in self.nodeClientList():
			for j in i["client"].containers.list():
				containerInfo = {"name":j.name,"node":i["name"]};
				reList.append(containerInfo);
		return reList;
	def servicesList(self):
		reList = [];
		for i in self.client.services.list():
			serviceInfo = {};
			serviceInfo["replicas"] = i.attrs["Spec"]["Mode"]["Replicated"]["Replicas"];
			serviceInfo["name"] = i.name;
			reList.append(serviceInfo)
		return reList;
	def servicesDetails(self):
		serviceslist = self.servicesList();
		containerlist = self.containerList();
		relist = [];
		for i in serviceslist:
			sinfo = {};
			sinfo["servicename"] = i["name"];
			sinfo["replicas"] = i["replicas"];
			sinfo["serviceinfo"] = [];
			for j in self.containerList():
				if j["name"].split(".")[0] == sinfo["servicename"]:
					sinfo["serviceinfo"].append(j);
			sinfo["replicas_running"] = len(sinfo["serviceinfo"]);
			relist.append(sinfo);
		return relist;
			
		

def searchSwarmMaster(nodelist,nodename):
	for i in nodelist:
                if i["name"] == nodename:
                        return gaSwarm(i["url"],i["version"],confList=nodelist);
	return 0;


	
