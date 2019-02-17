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
	$(".progress").fadeIn(500);
	$("#k_username").removeClass("invalid");
	$("#k_password").removeClass("invalid");

	var xxl = +$("#xxl").prop('checked');
	var email = +$("#email").prop('checked');
	var user = $("#k_username").val();
	var pass = ($("#k_password").val() == "         ") ? "" : $("#k_password").val();

	$.post({
		url: "/api/update_profile",
		data: JSON.stringify({"xxl": xxl, "email": email, "user": user, "pass": pass}),
		success: function(data) {
			if (!jQuery.isEmptyObject(data) && data["status"] == "Username or password incorrect") {
				$(".progress").fadeOut(500);
				Materialize.toast('Napačno uporabniško ime ali geslo!', 4000); // 4000 is the duration of the toast
				$("#k_username").addClass("invalid");
				$("#k_password").addClass("invalid");
			} else {
				$(".progress").fadeOut(500);
				Materialize.toast('Shranjeno!', 4000); // 4000 is the duration of the toast
			}
			
		},
		error: function() {
			$(".progress").fadeOut(500);
			Materialize.toast('Napaka! Poskusite kasneje', 4000); // 4000 is the duration of the toast
		},
		contentType: "application/json",
		dataType: "json"
	});
});

$("#order").click(function() {
	$(".progress").fadeIn(500);
	$.post({
		url: "/api/order",
		success: function(data) {
			$(".progress").fadeOut(500);
			if (!jQuery.isEmptyObject(data)) {
				var cas = parseInt(data["status"] / 60);
				switch(cas) {
					case 1:
						var min = " minuto";
						break;
					case 2:
						var min = " minuti";
						break;
					case 3:
					case 4:
						var min = " minute";
						break;
					default:
						var min = " minut";
				}
				Materialize.toast('Počakajte še ' + cas + min, 4000); // 4000 is the duration of the toast
			} else {
				Materialize.toast('Naročeno!', 4000); // 4000 is the duration of the toast
			}
		},
		error: function() {
			$(".progress").fadeOut(500);
			Materialize.toast('Napaka! Poskusite kasneje', 4000); // 4000 is the duration of the toast
		},
		contentType: "application/json",
		dataType: "json"
	});
});