function resetLevels() {
	var tmp = 0;			
	$("#levels > div").each(function() {
		tmp++;
		$(this).attr("id", "level"+tmp);
		$(this).find("h5").find("span").text("Nivo "+tmp);
	});
}

function checkLevelsLimit() {
	var limit = 5;

	var levelNum = $("#levels").children().length;
	if (levelNum >= limit) {
		$("#addLevel").addClass("disabled");
	} else {
		$("#addLevel").removeClass("disabled");
	}
}

var lastRemove;
function removeLevel() {
	$(lastRemove).parent().parent().remove();

	checkLevelsLimit();
	resetLevels();
}

function addLevel(tags = []) {
	var levelNum = $("#levels").children().length + 1;

	var chips = [];
	for (var i = 0; i < tags.length; i++) {
		chips[i] = {"tag": tags[i]};
	}

	$("#levels").append('<div id="level'+ levelNum +'"><h5><span>Nivo '+ levelNum +'</span><a href="#modal1" class="modal-trigger waves-effect waves-dark btn-flat right"><i class="material-icons">remove</i></a></h5><div class="chips"></div></div>');
	Materialize.fadeInImage('#level'+ levelNum);

	$('#level'+levelNum).find("div").material_chip({
		data: chips,
		placeholder: 'npr. Skutni štruklji',
		secondaryPlaceholder: 'Dodaj'
	});

	checkLevelsLimit();
}

function addBlacklist(tags = []) {
	var chips = [];
	for (var i = 0; i < tags.length; i++) {
		chips[i] = {"tag": tags[i]};
	}

	$("#blacklistLevels").append('<div id="blacklistLevel"><div class="chips"></div></div>');
	$('#blacklistLevel').find("div").material_chip({
		data: chips,
		placeholder: 'npr. Piščanec',
		secondaryPlaceholder: 'Dodaj'
	});
}

$.get({
	url: "/api/get_preferences",
	success: function(data) {
		$(".progress").fadeOut(500);
		if (data["index"].length > 0) {
			for (var i = 0; i < data["index"].length; i++) {
				addLevel(data["index"][i]);
			}
		} else {
			addLevel();
		}
		if (data["index"].length > 0) {
			addBlacklist(data["blacklist"]);
		} else {
			addBlacklist()
		}
	},
	dataType: "json"
});

// Initialize collapse button
$(".button-collapse").sideNav({
	menuWidth: 250
});

$('.modal').modal({
	ready: function(modal, trigger) { // Callback for Modal open. Modal and trigger parameters available.
		lastRemove = trigger;
	}
});

$('.dropdown-logout').dropdown({
	constrainWidth: false, // Does not change width of dropdown to that of the activator
	hover: true, // Activate on hover
	alignment: 'center' // Displays dropdown with edge aligned to the left of button
});

$("#addLevel").click(function () { addLevel(); });

$("#shrani, #shrani1").click(function() {
	$(".progress").fadeIn(500);
	var levels = [];
	$("#levels > div").each(function() {
		var tmp = [];
		var chipData = $(this).children(".chips").material_chip('data');
		if (chipData.length != 0) {
			for (var i = 0; i < chipData.length; i++) {
				tmp.push(chipData[i]["tag"]);
			}
			levels.push(tmp);
		} else {
			$(this).remove();

			checkLevelsLimit();
		}
	});

	resetLevels();

	var blacklist = [];
	var chipData = $("#blacklistLevel").children(".chips").material_chip('data');
	if (chipData.length != 0) {
		for (var i = 0; i < chipData.length; i++) {
			blacklist.push(chipData[i]["tag"]);
		}
	}

	$.post({
		url: "/api/update_preferences",
		data: JSON.stringify({"levels": levels, "blacklist": blacklist}),
		success: function() {
			$(".progress").fadeOut(500);
			Materialize.toast('Shranjeno!', 4000) // 4000 is the duration of the toast
		},
		error: function() {
			$(".progress").fadeOut(500);
			Materialize.toast('Napaka! Poskusite kasneje', 4000) // 4000 is the duration of the toast
		},
		contentType: "application/json",
		dataType: "json"
	});
});