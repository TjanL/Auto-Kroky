var url = "/api/getOrder.php";
$.get(url, function(data){
	$(".progress").fadeOut(500);
	if (!jQuery.isEmptyObject(data)) {
		$('#tableHead').html(data["weekStart"]+" - "+data["weekEnd"]);
		$('#update').html("Posodobljeno ob "+data["updated"]);

		$('#pon').html(data["log"][0]);
		$('#tor').html(data["log"][1]);
		$('#sre').html(data["log"][2]);
		$('#cet').html(data["log"][3]);
		$('#pet').html(data["log"][4]);	
	} else {
		$('#tableHead').html("Ni naročila");
	}
}, "json");

// Initialize collapse button
$(".button-collapse").sideNav({
	menuWidth: 250
});

$('.dropdown-logout').dropdown({
	constrainWidth: false, // Does not change width of dropdown to that of the activator
	hover: true, // Activate on hover
	alignment: 'center' // Displays dropdown with edge aligned to the left of button
});