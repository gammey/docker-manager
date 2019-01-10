imageV = new Vue({
	el: "#imageList",
	data:{
		imageInfo: [
		],
		controlURL: BASEAPI+"/docker/container/",
		seen: false,
	},
	methods:{
		delImage: function(index){
			id = this.imageInfo[index].id;
			node = this.imageInfo[index].nodename;
			url = "/image/"+node+"/"+id+"/delete/";	
			var that = this;
			modalV.message="操作中....";
			startload();
			axios({
				url: url,
				method: "post",
			})
			.then(function(resJson){
				//console.log(resJson);
                               if(resJson.data.status != 0)
                               {
                                    //alert(JSON.parse(resJson)["info"])
				    modalV.message=resJson.data.info;
                               }
			       else
				{
					that.imageInfo.splice(index,1);
					modalV.message="删除成功";
				}
                               stopload();
                        })	
			},
		historyImage: function(index){
			id = this.imageInfo[index].id;
			node = this.imageInfo[index].nodename;
			url = "/image/"+node+"/"+id+"/history/";	
			startload();
			$.ajax({
				url: url,
                                type: "POST",
				success: function(resJson){
                                        stopload();
                                        if(JSON.parse(resJson)["status"] == 0)
                                        {
                                                ans = JSON.parse(resJson)["info"];
						var reStr = "";
						console.log(ans);
						for(i in ans){
							reStr = reStr + ans[i]["CreatedBy"] + "<br/>"
						}
						alert(reStr);
                                        }
                                }
			})
		}
	}
})
