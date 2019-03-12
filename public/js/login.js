$("#login").click(function () {
	var username = $("#username").val()
	var password = $("#password").val()
	$.post({
		url: "/api/login",
		data: JSON.stringify({"username": username, "password": password}),
		success: function(data) {
			if (!jQuery.isEmptyObject(data)) {
				switch (data["status"]) {
					case "Logged in":
						window.location.replace("/");
						break;
					case "Username not registered":
						$("#username").addClass("invalid");
						$("username_helper").attr("data-error", data["status"]);
						break;
					case "Password incorrect":
						$("#password").addClass("invalid");
						$("#password_helper").attr("data-error", data["status"]);
						break;
				}
			} else {
				if ($("#username").val() == "") {
					$("#username").addClass("invalid");
					$("username_helper").attr("data-error", "Field empty");
				}
				if ($("#password").val() == "") {
					$("#password").addClass("invalid");
					$("#password_helper").attr("data-error", "Field empty");
				}
			}
		},
		error: function() {
			console.dir("Error");
		},
		contentType: "application/json",
		dataType: "json"
	});
});