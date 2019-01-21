#!/usr/bin/python
from conf import DockerList
from django.http import HttpResponse
import docker
import gaDocker
import gaSwarm
import json

def nodelist(request):
	relist=[];
	for i in DockerList:
		node = gaDocker.dockerNode(i["url"],i["version"]);
		nodeinfo={};
		nodeinfo['name']=i['name'];
		nodeinfo['url']=i["url"];
		nodeinfo['api-version']=i["version"];
		if i.has_key("role"):
			nodeinfo['role']=i["role"];
		else:
			nodeinfo["role"]="Normal Worker";
		try:
			nodeinfo["info"] = node.client.info();
			nodeinfo["status"] = "Running";
		except:
			nodeinfo["info"] = 0;
			nodeinfo["status"] = "Disconnect";
		relist.append(nodeinfo);
	response = HttpResponse(json.dumps(relist));	
	#response["Access-Control-Allow-Origin"] = "*";
	return response;

def containerDetailsList(request):
	redict = {};
	nodename=request.POST['nodename'].encode("utf-8");
	nodeSim = {};
	for i in DockerList:
		if i["name"] == nodename:
			nodeSim = i;
	if nodeSim.has_key("name") == False:
		redict["status"] = -1;
		redict["info"] = "UnKown nodename."
		return HttpResponse(json.dumps(redict));
	node = gaDocker.dockerNode(nodeSim["url"],nodeSim["version"]);
	redict["info"] = node.allContainerDetails();
	redict["status"] = 0;
	response = HttpResponse(json.dumps(redict));
        #response["Access-Control-Allow-Origin"] = "*";
	return response;
	
def imagesDetailsList(request):
	redict = {};
        nodename=request.POST['nodename'].encode("utf-8");
	for i in DockerList:
                if i["name"] == nodename:
                        nodeSim = i;
        if nodeSim.has_key("name") == False:
                redict["status"] = -1;
                redict["info"] = "UnKown nodename."
                return HttpResponse(json.dumps(redict));
        node = gaDocker.dockerNode(nodeSim["url"],nodeSim["version"]);
	redict["info"] = node.listImages();
        redict["status"] = 0;
	response = HttpResponse(json.dumps(redict));
	return response;

def servicesDetailsList(request,nodename):
	print nodename;
	redict = {};
	nodeSim = {};
	for i in DockerList:
                if i["name"] == nodename:
                        nodeSim = i;
        if nodeSim.has_key("name") == False:
                redict["status"] = -1;
                redict["info"] = "UnKown nodename."
                return HttpResponse(json.dumps(redict));
	node = gaDocker.dockerNode(nodeSim["url"],nodeSim["version"]);
        redict["info"] = node.listServices();
        redict["status"] = 0;
        response = HttpResponse(json.dumps(redict));
        return response;
	
def containerControl(request,nodename,containername,action):
	redict = {};
	node = gaDocker.searchNode(gaDocker.dockerlist,nodename);
	if node != 0:
		redict["status"]=0;
                redict["info"]="Success";
		if action == "start":
			if node.startContainer(containername) == 0:
                                redict["status"]=-1;
                                redict["info"]="Failed";
		elif action == "stop":
			if node.stopContainer(containername) == 0:
                                redict["status"]=-1;
                                redict["info"]="Failed";
		elif action == "restart":
			if node.restartContainer(containername) == 0:
                                redict["status"]=-1;
                                redict["info"]="Failed";
		elif action == "remove":
			if node.removeContainer(containername) == 0:
				redict["status"]=-1;
                        	redict["info"]="Failed";
		elif action == "detail":
			detail = node.getContainerFullDetail(containername);
			if detail != 0:
				redict["status"]=0;
                                redict["info"]=detail;
			else:
				redict["status"]=-1;
                                redict["info"]="Failed";
		else:
			redict["status"]=-1;
			redict["info"]="Unkown Action";
	else:
		redict["status"]=-1;
                redict["info"]="Unkown NodeName:"+nodename;
	response = HttpResponse(json.dumps(redict));
        #response["Access-Control-Allow-Origin"] = "*";
        return response;

def imageControl(request,nodename,imagename,action):
	redict = {};
        node = gaDocker.searchNode(gaDocker.dockerlist,nodename);
	redict["status"]=0;
        redict["info"]="Success";
	if action == "delete":
		res = node.delImage(imagename);
		if res != 0:
			redict["status"]=-1;
                        redict["info"]=res;
	elif action == "history":
		res = node.historyImage(imagename);
                if res != "Error":
                        redict["info"] = res;
			redict["status"] = 0;
                else:
			redict["status"] = -1;
			redict["info"] = "Error";
	else:
		redict["status"]=-1;
                redict["info"]="Unkown Action";
	response = HttpResponse(json.dumps(redict));
        return response;

def updateReplicas(request,nodename,servicename,replicas):
	node = gaDocker.searchNode(gaDocker.dockerlist,nodename);
	redict = {};
	if node == 0:
		redict["status"]=-1;
        	redict["info"]="Unkown Nodename";
		return redict;
	r = node.updateServiceReplicas(servicename,replicas);
	if r == 0:
		redict["status"]=0;
                redict["info"]="Success";
	else:
		redict["status"]=-1;
                redict["info"]="Failed";
	return HttpResponse(json.dumps(redict));

def updateImages(request,nodename,servicename,image):
	node = gaDocker.searchNode(gaDocker.dockerlist,nodename);
        redict = {};
        if node == 0:
                redict["status"]=-1;
                redict["info"]="Unkown Nodename";
                return redict;
        r = node.updateServiceImage(servicename,image);
        if r == 0:
                redict["status"]=0;
                redict["info"]="Success";
        else:
                redict["status"]=-1;
                redict["info"]="Failed";
        return HttpResponse(json.dumps(redict));

def swarmServicesProcessList(request,masterNodeName):
	swarm = gaSwarm.searchSwarmMaster(DockerList,masterNodeName)
	return HttpResponse(json.dumps(swarm.servicesDetails()));
