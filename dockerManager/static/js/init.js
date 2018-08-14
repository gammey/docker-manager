        $.ajax({
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
                        nodeV.getContainersDetails(0,false);
        },
        })
var vArr = [imageV,containersV];
function showV(varr,vobj){
        for (i in varr){
                console.log(varr[i]);
                varr[i].seen = false;
                }
        vobj.seen = true;
}
