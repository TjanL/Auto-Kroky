var url = "/api/get_order";
$.get({
	url: url,
	success: function(data) {
		$(".progress").fadeOut(500);
		if (!jQuery.isEmptyObject(data)) {
			if (!jQuery.isEmptyObject(data["log"])) {
				$('#tableHead').html(data["weekStart"]+" - "+data["weekEnd"]);
				$('#update').html("Posodobljeno ob "+data["updated"]);

				$('#pon').html(data["log"]["pon"]);
				$('#tor').html(data["log"]["tor"]);
				$('#sre').html(data["log"]["sre"]);
				$('#cet').html(data["log"]["cet"]);
				$('#pet').html(data["log"]["pet"]);	
			} else {
				$('#tableHead').html("Ni naročila");
			}
		} else {
			$('#tableHead').html("Ni naročila");
		}
	},
	dataType: "json"
});