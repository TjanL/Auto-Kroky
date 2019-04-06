$('.sidenav').sidenav();

$.get({
	url: "/api/get_user",
	success: function(data) {
		$(".username").text(data["username"]);
		$('.dropdown-trigger').dropdown({
            hover: true,
            constrainWidth: false
         });
		$('.dropdown-trigger-dots').dropdown({
			coverTrigger: false,
            constrainWidth: false
         });
	},
	dataType: "json"
});
         