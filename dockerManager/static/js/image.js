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
			startload();
			$.ajax({
				url: url,
				type: "POST",
				success: function(resJson){
					stopload();
					if(JSON.parse(resJson)["status"] != 0)
					{
						alert(JSON.parse(resJson)["info"])
					}
				}
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
