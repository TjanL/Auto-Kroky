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

$response = json_encode($_POST["levels"], JSON_UNESCAPED_UNICODE);
$blacklist = json_encode($_POST["blacklist"], JSON_UNESCAPED_UNICODE);

if((!is_array($_POST["levels"]) && $_POST["levels"] != "") || (!is_array($_POST["blacklist"]) && $_POST["blacklist"] != "")) {
	die("Oops! Something went wrong. Please try again later.");
}

$sql = "UPDATE config SET conf_index=?, blacklist=? WHERE id = ?";

if($stmt = mysqli_prepare($link, $sql)){
	mysqli_stmt_bind_param($stmt, "ssi", $response, $blacklist, $id);
	// Attempt to execute the prepared statement
	if(!mysqli_stmt_execute($stmt)) {
		echo "Oops! Something went wrong. Please try again later.";
	}
}
mysqli_stmt_close($stmt);

?>