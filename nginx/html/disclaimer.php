<?php
// Initialize the session
session_start();
 
// If session variable is not set it will redirect to login page
if(!isset($_SESSION['username']) || empty($_SESSION['username'])){
  header("location: /login");
  exit;
}
?>

<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
	<meta name="theme-color" content="#455a64">
	<meta property="og:locale" content="sl_SI">
	<meta property="og:url" content="https://autokroky.ddns.net">
	<meta property="og:type" content="website">
	<meta property="og:title" content="Auto Kroky avtomatsko naročanje malice">
	<meta property="og:description" content="Enostavno avtomatsko naročanje malice na Kroky.si">
	<meta property="og:image" content="https://autokroky.ddns.net/assets/ic_restaurant_black_128px.png">
	<meta name="description" content="Enostavno avtomatsko naročanje malice na Kroky.si">
	<meta name="author" content="Tjan Ljubešek">
	<link rel="shortcut icon" type="image/ico" href="/assets/favicon.ico"/>
	<title>Auto Kroky - Disclaimer</title>
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css">
	<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
	<link href="css/stylesheet.css" rel="stylesheet">
</head>

<body>
	<nav class="blue-grey darken-2">
		<a href="#" data-activates="slide-out" class="button-collapse"><i class="material-icons">menu</i></a>
		<i class="material-icons white-text brand-logo center hide-on-med-and-up show-on-medium">restaurant</i>
		<div class="nav-wrapper">
		  <ul class="right">
			<li><div id="username" class="grey darken-4 white-text chip center dropdown-logout" style="min-width: 80px;" data-activates='dropdown1'><?php echo htmlspecialchars($_SESSION['username']); ?></div></li>
			<ul id='dropdown1' class='dropdown-content'>
				<li><a href="/logout.php" class="grey-text text-darken-4"><i class="material-icons">exit_to_app</i>Odjava</a></li>
			</ul>
		  </ul>
		</div>
	</nav>

	<ul id="slide-out" class="side-nav fixed blue-grey darken-2 z-depth-0">
	  <li class="logo"><a class="white-text" href="/"><h5>Auto Kroky</h5></a></li>
	  <li><div class="divider transparent"></div></li>
	  <li><a class="white-text" href="/"><i class="material-icons white-text">restaurant</i>Pregled</a></li>
	  <li class="no-padding">
		<li><a class="dropdown-button white-text" data-activates="dropdown-settings"><i class="material-icons white-text">settings</i>Nastavitve<i class="material-icons right white-text">arrow_drop_down</i></a></li>
		<ul id='dropdown-settings' class='dropdown-content'>
			<li><a href="preferences"><i class="material-icons">tune</i>Naročanje</a></li>
			<li><a href="profile"><i class="material-icons">account_circle</i>Profil</a></li>
		</ul>
	</ul>
		
	<main class="grey-text text-darken-4">
		<div class="row">
			<div class="col offset-s0 s12 offset-m1 m10 offset-l1 l10">
				<h2 class="header">Disclaimer</h2>
				<p class="flow-text">
					We are not affiliated, associated, authorized, endorsed by, or in any way officially connected with K-NORMA D.O.O., or any of its subsidiaries or its affiliates. The official Kroky website can be found at http://www.kroky.si. The name “Kroky” as well as related names, marks, emblems and images are registered trademarks of K-NORMA D.O.O..
				</p>
				<p class="right">Made by Tjan Ljubešek</p>
			</div>
		</div>
		
	</main>
   
	<footer class="page-footer transparent" style="padding-top: 0;">
		<div class="footer-copyright">
			<div class="container">
				<div class="center"><label>© 2018 - <a class="grey-text" href="disclaimer">Disclaimer</a></label></div>
			</div>
		  </div>
	</footer>

</body>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js"></script>
<script>
	// Initialize collapse button
$(".button-collapse").sideNav({
	menuWidth: 250
});

$('.dropdown-logout').dropdown({
	constrainWidth: false, // Does not change width of dropdown to that of the activator
	hover: true, // Activate on hover
	alignment: 'center' // Displays dropdown with edge aligned to the left of button
});
</script>

</html>