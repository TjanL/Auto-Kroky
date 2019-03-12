$('.modal').modal();
$("#register").click(function () {
	var username = $("#username").val()
	var password = $("#password").val()
	var c_password = $("#confirm_password").val()
	var k_username = $("#k_username").val()
	var k_password = $("#k_password").val()

	$(".progress").removeClass("hide");
	$(".progress").fadeIn(500);

	$.post({
		url: "/api/register",
		data: JSON.stringify({
			"username": username,
			"password": password,
			"c_password": c_password,
			"k_username": k_username,
			"k_password": k_password
		}),
		success: function(data) {
			if (!jQuery.isEmptyObject(data)) {
				switch (data["status"]) {
					case "Registered":
						window.location.replace("/");
						break;
					case "Username already taken":
						$("#username").addClass("invalid");
						$("#username_helper").attr("data-error", data["status"]);
						break;
					case "Password must have atleast 6 characters":
						$("#password").addClass("invalid");
						$("#password_helper").attr("data-error", data["status"]);
						break;
					case "Passwords do not match":
						$("#confirm_password").addClass("invalid");
						$("#confirm_password_helper").attr("data-error", data["status"]);
						break;
					case "This username is already in use":
						$("#k_username").addClass("invalid");
						$("#k_username_helper").attr("data-error", data["status"]);
						break;
					case "Username or password incorrect":
						$("#k_password").addClass("invalid");
						$("#k_username").addClass("invalid");
						$("#k_username_helper").attr("data-error", data["status"]);
						break;
				}
			} else {
				if ($("#username").val() == "") {
					$("#username").addClass("invalid");
					$("#username_helper").attr("data-error", "Field empty");
				}
				if ($("#password").val() == "") {
					$("#password").addClass("invalid");
					$("#password_helper").attr("data-error", "Field empty");
				}
				if ($("#confirm_password").val() == "") {
					$("#confirm_password").addClass("invalid");
					$("#confirm_password_helper").attr("data-error", "Field empty");
				}
				if ($("#k_username").val() == "") {
					$("#k_username").addClass("invalid");
					$("#k_username_helper").attr("data-error", "Field empty");
				}
				if ($("#k_password").val() == "") {
					$("#k_password").addClass("invalid");
				}
			}
			$(".progress").fadeOut(500);
		},
		error: function() {
			console.dir("Error");
		},
		contentType: "application/json",
		dataType: "json"
	});
});