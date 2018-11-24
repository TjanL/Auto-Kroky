<?php
// Initialize the session
session_start();
 
// If session variable is not set it will redirect to login page
if(!isset($_SESSION['username']) || empty($_SESSION['username'])){
  header("location: /login");
  exit;
}

require_once realpath("/usr/local/nginx/sql_config.php");

$id = $_SESSION["id"];
$xxl = $_POST["xxl"];
$email = $_POST["email"];
$k_user = $_POST["user"];
$k_pass = $_POST["pass"];

if ($k_pass == "") {
	$sql = "UPDATE config SET k_username=?, xxl=?, email=? WHERE id = ?";
} else {
	$sql = "UPDATE config SET k_username=?, k_password=?, xxl=?, email=? WHERE id = ?";
}

if($stmt = mysqli_prepare($link, $sql)){
	if ($k_pass == "") {
		mysqli_stmt_bind_param($stmt, "ssii", $k_user, $xxl, $email, $id);
	} else {
		define('USER_AGENT', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36');
		define('LOGIN_FORM_URL', 'http://www.kroky.si/2016/?mod=register&action=login');
		define('LOGIN_ACTION_URL', 'http://www.kroky.si/2016/?mod=register&action=login');

		$postValues = array(
		    'username' => $k_user,
		    'password' => $k_pass
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
		
		if (trim($confirmation->textContent) == "Prijava je uspela.") {
			mysqli_stmt_bind_param($stmt, "ssiii",  $k_user, $k_pass, $xxl, $email, $id);
		} else {
			echo "Login error";
		}
	}
	// Attempt to execute the prepared statement
	if(!mysqli_stmt_execute($stmt)) {
		//echo "Oops! Something went wrong. Please try again later.";
	}
}
mysqli_stmt_close($stmt);

?>