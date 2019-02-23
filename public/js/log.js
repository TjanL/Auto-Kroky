var url = "/api/get_order";
$.get({
	url: url,
	success: function(data) {
		$(".progress").fadeOut(500);
		console.dir(data);
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

// Initialize collapse button
$(".button-collapse").sideNav({
	menuWidth: 250
});

$('.dropdown-logout').dropdown({
	constrainWidth: false, // Does not change width of dropdown to that of the activator
	hover: true, // Activate on hover
	alignment: 'center' // Displays dropdown with edge aligned to the left of button
});