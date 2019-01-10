function startload(){
	document.getElementById('spin').style.display='block'
	document.getElementById('mainbody').style.display='none'
}
function stopload(){
	document.getElementById('spin').style.display='none'
	document.getElementById('mainbody').style.display='block'
}
var BASEAPI=""
nodeV = new Vue({
	el: "#nodeList",
	data:{
		nodeInfo: [
			
		],
	},
	methods: {
		getImageDetails: function(index){
                	showV(vArr,imageV);
			nodename = this.nodeInfo[index].name;
			startload();
			$.ajax({
				url: BASEAPI+"/docker/image/detail",
				type: "POST",
				data: {	nodename: nodename,	},
				success: function(resJson){
					res = JSON.parse(resJson)["info"];
					imageV.imageInfo = [];
					for (i in res)
					{
						var image = {};
						image["nodename"] = nodename;
						if ( res[i]["Id"].indexOf(":") > 0 )
						{
							image["id"] = res[i]["Id"].split(":")[1];
						}
						else
						{
							image["id"] = res[i]["Id"];
						}
						//console.log(image["id"]);
						if ( res[i]["RepoTags"].length > 0)
						{
							image["name"] = res[i]["RepoTags"][0];
							image["version"] = res[i]["RepoTags"][0].split(":")[res[i]["RepoTags"][0].split(":").length-1];
						}
						else
						{
							image["name"] = image["id"];
							image["version"] = "Unkown";
						}
						image["size"] = (res[i]["VirtualSize"]/1024/1024).toFixed(2);
						image["createTime"] = res[i]["Created"];
						imageV.imageInfo.push(image);
					}
					stopload();
				}	

			})
		},
		getServiceDetails(index,refresh=true){
			if (refresh == true){
                                showV(vArr,serviceV);
                        }
			url = BASEAPI+"/docker/service/"+this.nodeInfo[index].name+"/";
			nodename = this.nodeInfo[index].name;
			axios.get(url)
			.then(function(response){
				serviceV.serviceInfo=[];
				for (i in response.data.info)
				{
					var srv = {};
					var r = response.data.info[i]
					console.log(r);
					srv["managenode"] = nodename;
					srv["name"] = r.Spec.Name;
					srv["id"] = r["ID"];
					srv["replicas"] = r.Spec.Mode.Replicated.Replicas;
					srv["labels"] = r.Spec.Labels["com.docker.stack.namespace"];
					srv["image"] = r.Spec.TaskTemplate.ContainerSpec.Image.split("@")[0];
					srv["Expose"] = [];
					for (j in r.Endpoint.Ports)
					{
						var rs = r.Endpoint.Ports[j];
						var expose = {};
						expose["TargetPort"] = rs["TargetPort"];
						expose["PublishedPort"] = rs["PublishedPort"];
						expose["Protocol"] = rs["Protocol"];
						expose["PublishMode"] = rs["PublishMode"];
						srv["Expose"].push(expose);
					}
					srv["mount"] = [];
					for (j in r.Spec.TaskTemplate.ContainerSpec.Mounts)
					{
						var rm = r.Spec.TaskTemplate.ContainerSpec.Mounts[j];
						var m = {};
						m["Source"] = rm["Source"];
						m["Target"] = rm["Target"];
						m["Type"] = rm["Type"];
						srv["mount"].push(m);
					}
					//console.log("Before Push srv"+srv["mount"]);
					serviceV.serviceInfo.push(srv);
					serviceV.serviceInfo.sort(compare("labels"));
				}
			})
			.catch(function(err){
				console.log(err);
			})
			//console.log(serviceV.serviceInfo[0]);
		},
		getContainersDetails(index,refresh=true){
			if (refresh == true){
				showV(vArr,containersV);
			}
			nodename = this.nodeInfo[index].name;
			startload();
			$.ajax({
				url: BASEAPI+"/docker/container/detail",
				type:"POST",
				data:{
					nodename: nodename,
				},
				success:function(resJson){
					res = JSON.parse(resJson)["info"];
					containersV.containersInfo=[];
					for (i in res){
						var container = {};
						container["name"]=res[i]["name"];
						container["nodename"]=nodename;
						container["status"]=res[i]["detail"]["State"]["Status"].toUpperCase();
						if(container["status"] == "RUNNING"){
							container["startDisable"] = true;
							container["stopDisable"] = false;
							container["restartDisable"] = false;
							container["delDisable"] = true;
						}
						else{
							container["startDisable"] = false;
							container["stopDisable"] = true;
							container["restartDisable"] = true;
							container["delDisable"] = false;
						}
						if ( container["name"] == "docker-manager")
						{
							container["stopDisable"] = true;
                                                        container["restartDisable"] = true;

						}
						container["id"]=res[i]["detail"]["Id"];
						container["image"]=res[i]["detail"]["Config"]["Image"];
						container["ctime"]=res[i]["detail"]["Created"];
						container["starttime"]=res[i]["detail"]["State"]["StartedAt"];
						container["memuse"]=(res[i]["stats"]["memory_stats"]["usage"]/1024/1024).toFixed(2);
						container["mempercent"]=(res[i]["stats"]["memory_stats"]["usage"]/res[i]["stats"]["memory_stats"]["limit"]*100).toFixed(2);
						containersV.containersInfo.push(container);
						stopload()
					}
				}
			})
		
		}
	}
})
containersV = new Vue({
	el: "#containerList",
	data:{
		containersInfo: [
			{"name":"container1","nodename":"node1","notRunning":false,"notRunning":true},
		],
		controlURL: BASEAPI+"/container/",
		seen: true,
	},
	methods: {
		containerAction: function(index,action){
			nodename = this.containersInfo[index].nodename;
			containername = this.containersInfo[index].name;
			url = this.controlURL+nodename+"/"+containername+"/"+action+"/";
			startload();
			$.ajax({
				url: url,
				type:"POST",
				success:function(resJSON){
					containersV.containerRefresh(index);
					if(action == "remove"){
						containersV.containersInfo.splice(index,1);
					}
					stopload();
					modalV.message = "删除成功";
				}
			})
		},
		containerRefresh: function(index){
			odename = this.containersInfo[index].nodename;
			containername = this.containersInfo[index].name;
			url = this.controlURL+nodename+"/"+containername+"/detail/";
			$.ajax({
				url: url,
				type:"POST",
				success:function(resJSON){
					if(JSON.parse(resJSON)["status"]==0)
					{
						res = JSON.parse(resJSON)["info"];
						//console.log(res["State"]["Status"].toUpperCase());
						containersV.containersInfo[index].status = res["detail"]["State"]["Status"].toUpperCase();
						containersV.containersInfo[index].starttime = res["detail"]["State"]["StartedAt"];
						containersV.containersInfo[index].memuse = (res["stats"]["memory_stats"]["usage"]/1024/1024).toFixed(2);
						containersV.containersInfo[index].mempercent = (res["stats"]["memory_stats"]["usage"]/res["stats"]["memory_stats"]["limit"]*100).toFixed(2);
						if(containersV.containersInfo[index].status == "RUNNING"){
							containersV.containersInfo[index]["startDisable"] = true;
							containersV.containersInfo[index]["stopDisable"] = false;
							containersV.containersInfo[index]["restartDisable"] = false;
							containersV.containersInfo[index]["delDisable"] = true;
						}
						else{
							containersV.containersInfo[index]["startDisable"] = false;
							containersV.containersInfo[index]["stopDisable"] = true;
							containersV.containersInfo[index]["restartDisable"] = true;
							containersV.containersInfo[index]["delDisable"] = false;
						}
					}
				}
			})
		}
	}
})
/*	$.ajax({
		url: BASEAPI+"/docker/list",
		type:"POST",
		success:function(resJSON){
			res = JSON.parse(resJSON);
			for (i in res){
				var node = {};
				node['name'] = res[i]['name'];
				node['url'] = res[i]['url'];
				node['version'] = res[i]['api-version'];
				node['allContainers'] = res[i]['info']['Containers'];
				node['status'] = res[i]['status'];
				if (res[i]["info"].hasOwnProperty("ContainersRunning") == true)
				{
					node['runningContainers'] = res[i]["info"]["ContainersRunning"];
				}
				else{
					node['runningContainers'] = "UnKown";
				}
				nodeV.nodeInfo.push(node);
			}
			nodeV.getContainersDetails(0);
        },
	}) */
