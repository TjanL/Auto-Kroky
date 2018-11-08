var url = "/malica/api/latestOrder";
$.get(url, function(data){
	$('#img').attr("src", "/malica/screenshots/"+data["img"]);
	$('#tableHead').html(data["dateStart"]+" - "+data["dateEnd"]);

	$('#pon').html(data["order"][0]);
	$('#tor').html(data["order"][1]);
	$('#sre').html(data["order"][2]);
	$('#cet').html(data["order"][3]);
	$('#pet').html(data["order"][4]);	
}, "json");