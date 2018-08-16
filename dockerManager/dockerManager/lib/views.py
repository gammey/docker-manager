#!/usr/bin/python
from conf import DockerList
from django.http import HttpResponse
import docker
import gaDocker
import json

def nodelist(request):
	relist=[];
	for i in DockerList:
		node = gaDocker.dockerNode(i["url"],i["version"]);
		nodeinfo={};
		nodeinfo['name']=i['name'];
		nodeinfo['url']=i["url"];
		nodeinfo['api-version']=i["version"];
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
	else:
		redict["status"]=-1;
                redict["info"]="Unkown Action";
	response = HttpResponse(json.dumps(redict));
        return response;
