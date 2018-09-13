serviceV = new Vue({
	el: "#serviceList",
	data:{
		serviceInfo: [
		],
		controlURL: BASEAPI+"/service/",
		seen: false,
	},
	methods:{
		updateRplicas: function(index){
			srv = this.serviceInfo[index];
			console.log(this.serviceInfo[index].replicas);
			url = "/service/update/"+ srv.managenode+"/" + srv.name + "/replicas/" + srv.replicas + "/"
			axios.get(url)
			.then(function(response) {
				modalV.message = response.data;
				nodeV.getServiceDetails();
			}).catch(function (error) {
    				console.log(error);
  			});
		}	

	}
})
