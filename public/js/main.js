$.get({
	url: "/api/get_user",
	success: function(data) {
		$("#username").text(data["username"]);
	},
	dataType: "json"
});