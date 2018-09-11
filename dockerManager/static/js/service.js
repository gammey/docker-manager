serviceV = new Vue({
	el: "#serviceList",
	data:{
		serviceInfo: [
		],
		controlURL: BASEAPI+"/docker/service/",
		seen: false,
	}
})
