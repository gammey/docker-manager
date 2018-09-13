modalV = new Vue({
	el: "#publicModal",
	data:{
		message: '',
	}
}) 

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
                                node['role'] = res[i]['role'];
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
var vArr = [imageV,containersV,serviceV];
function showV(varr,vobj){
        for (i in varr){
                varr[i].seen = false;
                }
        vobj.seen = true;
}

function compare(propertyName) {
  return function(object1, object2) {
    var value1 = object1[propertyName];
    var value2 = object2[propertyName];
    if (value2 < value1) {
      return 1;
    } else if (value2 > value1) {
      return -1;
    } else {
      return 0;     
    }
  }
}
