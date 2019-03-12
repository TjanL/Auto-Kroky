$.get({
	url: "/api/get_profile",
	success: function(data){
		$(".progress").fadeOut(500);
		if (!jQuery.isEmptyObject(data)) {	
			$("#k_username").val(data["k_username"]);
			$("#k_password").val("         ");

			$("#email").prop('checked', data["email"]);
			$("#xxl").prop('checked', data["xxl"]);
		}
	},
	dataType: "json"
});

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
				M.toast({html: 'Napačno uporabniško ime ali geslo!'});
				$("#k_username").addClass("invalid");
				$("#k_password").addClass("invalid");
			} else {
				$(".progress").fadeOut(500);
				M.toast({html: 'Shranjeno!'});
			}
			
		},
		error: function() {
			$(".progress").fadeOut(500);
			M.toast({html: 'Napaka! Poskusite kasneje'});
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
				M.toast({html: 'Počakajte še ' + cas + min});
			} else {
				M.toast({html: 'Naročeno!'});
			}
		},
		error: function() {
			$(".progress").fadeOut(500);
			M.toast({html: 'Napaka! Poskusite kasneje'});
		},
		contentType: "application/json",
		dataType: "json"
	});
});