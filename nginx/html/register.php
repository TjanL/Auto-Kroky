<?php
// Include config file
require_once realpath("/usr/local/nginx/sql_config.php");
 
// Define variables and initialize with empty values
$username = $password = $confirm_password = "";
$username_err = $password_err = $confirm_password_err = $k_err = "";
 
// Processing form data when form is submitted
if($_SERVER["REQUEST_METHOD"] == "POST") {
 
	// Validate username
	if(empty(trim($_POST["username"]))){
		$username_err = "Please enter a username";
	} else{
		// Prepare a select statement
		$sql = "SELECT id FROM users WHERE username = ?";
		
		if($stmt = mysqli_prepare($link, $sql)){
			// Bind variables to the prepared statement as parameters
			mysqli_stmt_bind_param($stmt, "s", $param_username);
			
			// Set parameters
			$param_username = trim($_POST["username"]);
			
			// Attempt to execute the prepared statement
			if(mysqli_stmt_execute($stmt)){
				/* store result */
				mysqli_stmt_store_result($stmt);
				
				if(mysqli_stmt_num_rows($stmt) == 1){
					$username_err = "This username is already taken";
				} else{
					$username = trim($_POST["username"]);
				}
			} else{
				echo "Oops! Something went wrong. Please try again later";
			}
		}
		 
		// Close statement
		mysqli_stmt_close($stmt);
	}
	
	// Validate password
	if(empty(trim($_POST['password']))){
		$password_err = "Please enter a password";
		   
	} elseif(strlen(trim($_POST['password'])) < 6){
		$password_err = "Password must have atleast 6 characters";
		
	} else{
		$password = trim($_POST['password']);
	}
	
	// Validate confirm password
	if(empty(trim($_POST["confirm_password"]))){
		$confirm_password_err = "Please confirm password";
	} else{
		$confirm_password = trim($_POST['confirm_password']);
		if($password != $confirm_password){
			$confirm_password_err = "Password did not match";
		}
	}

	// Validate Kroky username and password
	if (empty(trim($_POST["k_username"])) && empty(trim($_POST["k_password"]))) {
		$k_err = "Please enter the password and username";
	} else {
		// Prepare a select statement
		$sql = "SELECT id FROM config WHERE k_username = ?";
		
		if($stmt = mysqli_prepare($link, $sql)){
			// Bind variables to the prepared statement as parameters
			mysqli_stmt_bind_param($stmt, "s", $param_k_username);
			
			// Set parameters
			$param_k_username = trim($_POST["k_username"]);
			
			// Attempt to execute the prepared statement
			if(mysqli_stmt_execute($stmt)){
				/* store result */
				mysqli_stmt_store_result($stmt);
				
				if(mysqli_stmt_num_rows($stmt) == 1){
					$k_err = "This username is already used";
					$k_username = trim($_POST["k_username"]);
				} else{
					//$k_username = trim($_POST["k_username"]);
					define('USER_AGENT', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36');
					define('LOGIN_FORM_URL', 'http://www.kroky.si/2016/?mod=register&action=login');
					define('LOGIN_ACTION_URL', 'http://www.kroky.si/2016/?mod=register&action=login');

					$postValues = array(
					    'username' => trim($_POST["k_username"]),
					    'password' => trim($_POST["k_password"])
					);
					 
					//Initiate cURL.
					$curl = curl_init();
					
					curl_setopt($curl, CURLOPT_URL, LOGIN_ACTION_URL);
					
					curl_setopt($curl, CURLOPT_POST, true);
					
					curl_setopt($curl, CURLOPT_POSTFIELDS, http_build_query($postValues));
					
					curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
					curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
					
					curl_setopt($curl, CURLOPT_USERAGENT, USER_AGENT);
					 
					//Tells cURL to return the output once the request has been executed.
					curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
					
					libxml_use_internal_errors(true);

					$html = new DOMDocument();
					$html->loadHTML(curl_exec($curl));
					
					//Check for errors
					if(curl_errno($curl)){
					    throw new Exception(curl_error($curl));
					}

					$xpath = new DOMXPath($html);
					$confirmation = $xpath->query("//body/h1")->item(0);
					
					if (trim($confirmation->textContent) != "Prijava je uspela.") {
						$k_err = "Username or password incorrect";
					}
				}
			} else{
				echo "Oops! Something went wrong. Please try again later";
			}
		}
	}
	
	// Check input errors before inserting in database
	if(empty($username_err) && empty($password_err) && empty($confirm_password_err) && empty($k_err)) {
		
		// Prepare an insert statement
		$sql = "INSERT INTO users (username, password) VALUES (?, ?)";
		 
		if($stmt = mysqli_prepare($link, $sql)){
			// Bind variables to the prepared statement as parameters
			mysqli_stmt_bind_param($stmt, "ss", $param_username, $param_password);
			
			// Set parameters
			$param_username = $username;
			$param_password = password_hash($password, PASSWORD_DEFAULT); // Creates a password hash
			
			// Attempt to execute the prepared statement
			if(mysqli_stmt_execute($stmt)){
				$sql = "INSERT INTO config (k_username,k_password) VALUES (?, ?)";
		 
				if($stmt1 = mysqli_prepare($link, $sql)){
					// Bind variables to the prepared statement as parameters
					mysqli_stmt_bind_param($stmt1, "ss", $param_k_username, $param_k_password);
					
					// Set parameters
					$param_k_username = trim($_POST["k_username"]);
					$param_k_password = trim($_POST["k_password"]);
					
					// Attempt to execute the prepared statement
					if(mysqli_stmt_execute($stmt1)){
						// Redirect to login page
						header("location: login.php");
					} else {
						echo "Something went wrong. Please try again later.";
					}
				}
				// Close statement
				mysqli_stmt_close($stmt1);
			} else {
				echo "Something went wrong. Please try again later.";
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
	<title>Registracija - Auto Kroky</title>
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
						<span class="card-title">Registracija</span>
					</div>
					<div class="card-content">
						<form id="register" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
							<div class="input-field">
								<input placeholder="Uporabniško ime" type="text" id="username" name="username" class="validate <?php echo (!empty($username_err)) ? 'invalid' : ''; ?>" value="<?php echo $username; ?>">
								<label for="username" data-error="<?php echo (!empty($username_err)) ? $username_err : ''; ?>"></label>
							</div>
							<div class="input-field">
								<input placeholder="Geslo" type="password" id="password" name="password" class="validate <?php echo (!empty($password_err)) ? 'invalid' : ''; ?>" value="<?php echo $password; ?>">
								<label for="password" data-error="<?php echo (!empty($password_err)) ? $password_err : ''; ?>"></label>
							</div>
							<div class="input-field">
								<input placeholder="Ponovite geslo" type="password" id="confirm_password" name="confirm_password" class="validate <?php echo (!empty($confirm_password_err)) ? 'invalid' : ''; ?>" value="<?php echo $confirm_password; ?>">
								<label for="confirm_password" data-error="<?php echo (!empty($confirm_password_err)) ? $confirm_password_err : ''; ?>"></label>
							</div>
							<div class="divider"></div>
							<div>
								<h5>Kroky</h5>
								<p>Za preverjanje pristnosti računa in prijavo pri samodejnem naročanju vnesite uporabniško ime in geslo vašega Kroky računa.</p>
							</div>
							<div class="input-field">
								<input placeholder="Kroky uporabniško ime" type="text" id="k_username" name="k_username" class="validate <?php echo (!empty($k_err)) ? 'invalid' : ''; ?>" value="<?php echo $k_username; ?>">
								<label for="k_username" data-error="<?php echo (!empty($k_err)) ? $k_err : ''; ?>"></label>
							</div>
							<div class="input-field">
								<input placeholder="Kroky geslo" type="password" id="k_password" name="k_password" class="validate <?php echo (!empty($k_err)) ? 'invalid' : ''; ?>">
							</div>
							<div>
								<input type="submit" class="hide">
								<a href="#warning" class="modal-trigger waves-effect waves-light btn blue-grey lighten-1">Registriraj se</a>

								<div id="warning" class="modal">
									<div class="modal-content">
									  <h4>POZOR</h4>
									  <p>VAŠE KROKY UPORABNIŠKO IME IN GESLO SE SHRANITA NA STREŽNIK, KI GA NE NADZIRA <b>K-NORMA d.o.o</b> OZIROMA <b>Kroky.si</b>.</p>
									  <p>Z nadaljevanjem se strinjate, da vse storitve uporabljate na lastno odgovornost.</p>
									</div>
									<div class="modal-footer">
									  <a href="login.php" class="modal-action modal-close waves-effect waves-dark btn-flat blue-text">Ne strinjam se</a>
									  <button class="modal-action modal-close waves-effect waves-dark btn-flat blue-text" type="submit" name="register">Se strinjam</button>
									</div>
								</div>
							</div>
						</form>
					</div>
					<div class="card-content"><p>Already have an account? <a href="login">Login here</a></p></div>
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
<script type="text/javascript">$('.modal').modal();</script>

</html>