$.get({
	url: "/api/get_profile",
	success: function(data){
		$(".progress").fadeOut(500);
		if (!jQuery.isEmptyObject(data)) {	
			$('select').material_select();
			$("#k_username").val(data["k_username"]);
			$("#k_password").val("         ");

			$("#email").prop('checked', data["email"]);
			$("#xxl").prop('checked', data["xxl"]);
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

$('select').material_select();

$("#shrani").click(function() {
	$("#k_username").removeClass("invalid");
	$("#k_password").removeClass("invalid");

	var xxl = +$("#xxl").prop('checked');
	var email = +$("#email").prop('checked');
	var user = $("#k_username").val();
	var pass = ($("#k_password").val() == "         ") ? "" : $("#k_password").val();

	$.post({
		url: "/api/update_profile",
		data: JSON.stringify({"xxl": xxl, "email": email, "user": user,"pass": pass}),
		success: function(data) {
			if (data != "Login error") {
				Materialize.toast('Shranjeno!', 4000) // 4000 is the duration of the toast
			} else {
				$("#k_username").addClass("invalid");
				$("#k_password").addClass("invalid");
			}
		},
		error: function() {
			Materialize.toast('Napaka! Poskusite kasneje', 4000) // 4000 is the duration of the toast
		},
		contentType: "application/json",
		dataType: "json"
	});

$("#order").click(function() {
	$(".progress").fadeIn(500);
	$.post("/api/runAutoMalica.php")
		.done(function(data) {
			$(".progress").fadeOut(500);
			if (data != "") {
				data = parseInt(data/60)
				switch(data) {
					case "1":
						var min = " minuto";
						break;
					case "2":
						var min = " minuti";
						break;
					case "3":
					case "4":
						var min = " minute";
						break;
					default:
						var min = " minut";
				}
				Materialize.toast('Počakajte še ' + data + min, 4000) // 4000 is the duration of the toast
			} else {
				Materialize.toast('Naročeno!', 4000) // 4000 is the duration of the toast
			}
		})
		.fail(function() {
			$(".progress").fadeOut(500);
			Materialize.toast('Napaka! Poskusite kasneje', 4000) // 4000 is the duration of the toast
		});
});