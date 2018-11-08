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
	<title>Profil - Auto Kroky</title>
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css">
	<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
	<link href="/css/stylesheet.css" rel="stylesheet">
</head>

<body>
	<nav class="blue-grey darken-2">
		<a href="#" data-activates="slide-out" class="button-collapse"><i class="material-icons">menu</i></a>
		<i class="material-icons white-text brand-logo center hide-on-med-and-up show-on-medium">restaurant</i>
		<div class="nav-wrapper">
		  <ul class="right">
			<li><div id="username" class="grey darken-4 white-text chip center dropdown-logout" style="min-width: 80px;" data-activates='dropdown1'><?php echo htmlspecialchars($_SESSION['username']); ?></div></li>
			<ul id='dropdown1' class='dropdown-content'>
				<li><a href="logout" class="grey-text text-darken-4"><i class="material-icons">exit_to_app</i>Odjava</a></li>
			</ul>
		  </ul>
		</div>
	</nav>

	<ul id="slide-out" class="side-nav fixed blue-grey darken-2 z-depth-0">
	  <li class="logo"><a class="white-text" href="/"><h5>Auto Kroky</h5></a></li>
	  <li><div class="divider transparent"></div></li>
	  <li><a class="white-text" href="/"><i class="material-icons white-text">restaurant</i>Pregled</a></li>
	  <li class="no-padding">
		<li><a class="dropdown-button white-text" href="" data-activates="dropdown-settings"><i class="material-icons white-text">settings</i>Nastavitve<i class="material-icons right white-text">arrow_drop_down</i></a></li>
		<ul id='dropdown-settings' class='dropdown-content'>
			<li><a href="preferences"><i class="material-icons">tune</i>Naročanje</a></li>
			<li><a href=""><i class="material-icons">account_circle</i>Profil</a></li>
		</ul>
	</ul>
		
	<main class="grey-text text-darken-4">
		<div class="row">
			<div class="col offset-s0 s12 offset-m2 m8 offset-l3 l6">
				<h3>Profil</h3>
				<div class="row">
					<div style="min-height: 4px;margin: .5rem 0 1rem 0;">
						<div class="progress">
							<div class="indeterminate"></div>
						</div>
					</div>
					<div class="col s5">
						<span><b>Kroky</b> uporabniško ime:</span>
					</div>
					<div class="col s7">
						<input placeholder="Uporabniško ime" type="text" id="k_username">
					</div>
					<div class="col s5">
						<span><b>Kroky</b> geslo:</span><br><label>WIP - gesla shranjena v navadem tekstu</label>
					</div>
					<div class="col s7">
						<input placeholder="Geslo" type="password" id="k_password">
					</div>
					<div class="row"></div>
					<div class="col s10">
						<span>Pošlji naročilo na e-mail</span>
					</div>
					<div class="col s2">
						<div class="switch right">
						<label>
							<input id="email" type="checkbox">
							<span class="lever"></span>
						</label>
						</div>
					</div>
					<div class="row"></div>
					<div class="col s10">
						<span>Naroči XL in XXL malico</span>
						<br>
						<label>Kroky XL doplačilo 0,50€ / XXL doplačilo 1,00€ na malico</label>
					</div>
					<div class="col s2">
						<div class="switch right">
						<label>
							<input id="xxl" type="checkbox">
							<span class="lever"></span>
						</label>
						</div>
					</div>
					<div class="row"></div>
					<div class="col s8">
						<span>Ponovno naroči</span>
						<br>
						<label>Ponovno naročanje je mogoče le vsakih 15 minut</label>
					</div>
					<div class="col s4">
						<a id="order" class="waves-effect waves-light btn right">Naroči</a>
					</div>
				</div>
			</div>
		</div>
		<div class="row">
			<div class="col offset-s0 s12 offset-m2 m8 offset-l3 l6">
				<a id="shrani" class="waves-effect waves-light btn blue-grey lighten-1 right">Shrani</a>
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
<script src="js/profile.js"></script>

</html>