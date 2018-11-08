<?php
// Include config file
require_once realpath("/usr/local/nginx/sql_config.php");
 
// Define variables and initialize with empty values
$username = $password = "";
$username_err = $password_err = "";
 
// Processing form data when form is submitted
if($_SERVER["REQUEST_METHOD"] == "POST"){
 
	// Check if username is empty
	if(empty(trim($_POST["username"]))){
		$username_err = 'Please enter username';
	} else{
		$username = trim($_POST["username"]);
	}
	
	// Check if password is empty
	if(empty(trim($_POST['password']))){
		$password_err = 'Please enter your password';
	} else{
		$password = trim($_POST['password']);
	}
	
	// Validate credentials
	if(empty($username_err) && empty($password_err)){
		// Prepare a select statement
		$sql = "SELECT username, password, id FROM users WHERE username = ?";
		
		if($stmt = mysqli_prepare($link, $sql)){
			// Bind variables to the prepared statement as parameters
			mysqli_stmt_bind_param($stmt, "s", $param_username);
			
			// Set parameters
			$param_username = $username;
			
			// Attempt to execute the prepared statement
			if(mysqli_stmt_execute($stmt)){
				// Store result
				mysqli_stmt_store_result($stmt);
				
				// Check if username exists, if yes then verify password
				if(mysqli_stmt_num_rows($stmt) == 1){
					// Bind result variables
					mysqli_stmt_bind_result($stmt, $username, $hashed_password, $id);
					if(mysqli_stmt_fetch($stmt)){
						if(password_verify($password, $hashed_password)){
							/* Password is correct, so start a new session and
							save the username to the session */
							session_start();
							$_SESSION['username'] = $username;
							$_SESSION['id'] = $id;
							header("location: /");
						} else{
							// Display an error message if password is not valid
							$password_err = 'The password you entered was not valid';
						}
					}
				} else{
					// Display an error message if username doesn't exist
					$username_err = 'No account found with that username';
				}
			} else{
				echo "Oops! Something went wrong. Please try again later.";
			}
		}
		
		// Close statement
		mysqli_stmt_close($stmt);
	}
	
	// Close connection
	mysqli_close($link);
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
	<title>Prijava - Auto Kroky</title>
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css">
	<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
	<link href="css/login.css" rel="stylesheet">
</head>

<body>
	<main class="grey-text text-darken-4">
		<div class="row"></div>
		<div class="row">
			<div class="col s12 offset-m3 m6 offset-l4 l4">
				<div class="center-align">
					<h1 class="page-title" style="font-weight: 100;">Auto Kroky</h1>
				</div>
			</div>
		</div>
		<div class="row">
			<div class="col s12 offset-m3 m6 offset-l4 l4">
				<div class="card">
					<div class="card-image blue-grey darken-2" style="height: 6rem;">
            			<span class="card-title">Prijava</span>
            		</div>
	            	<div class="card-content">
						<form id="login" action="<?php echo htmlspecialchars($_SERVER['PHP_SELF']); ?>" method="post">
							<div class="input-field">
								<input placeholder="Uporabniško ime" type="text" id="username" name="username" class="validate <?php echo (!empty($username_err)) ? 'invalid' : ''; ?>" value="<?php echo $username; ?>">
								<label for="username" data-error="<?php echo (!empty($username_err)) ? $username_err : ''; ?>"></label>
							</div>
							<div class="input-field">
								<input placeholder="Geslo" id="password" name="password" type="password" class="validate <?php echo (!empty($password_err)) ? 'invalid' : ''; ?>">
								<label for="password" data-error="<?php echo (!empty($password_err)) ? $password_err : ''; ?>"></label>
							</div>
							<div>
								<button class="waves-effect waves-light btn blue-grey lighten-1" type="submit" name="login">Vpis</button>
							</div>
						</form>
					</div>
					<div class="card-content"><p>Don't have an account? <a href="register">Sign up now</a></p></div>
				</div>
			</div>
		</div>		
	</main>

	<footer class="page-footer transparent" style="padding-top: 0;">
		<div class="footer-copyright transparent">
			<div class="container">
				<div class="center"><img src="/assets/ic_restaurant_black_48px.svg"></div>
				<div class="center">
					<label>
						We are not affiliated, associated, authorized, endorsed by, or in any way officially connected with K-NORMA D.O.O., or any of its subsidiaries or its affiliates. The official Kroky website can be found at http://www.kroky.si. The name “Kroky” as well as related names, marks, emblems and images are registered trademarks of K-NORMA D.O.O..
					</label>
				</div>
			</div>
		  </div>
	</footer>
</body>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js"></script>

</html>