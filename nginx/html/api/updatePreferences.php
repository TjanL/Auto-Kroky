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
$response = $_POST["levels"];

for ($i=0; $i < count($response); $i++) { 
	$response[$i] = join("|",$response[$i]);
}

$blacklist = join("|",$_POST["blacklist"]);

$sql = "UPDATE config SET `1`=?, `2`=?, `3`=?, `4`=?, `5`=?, blacklist=? WHERE id = ?";

if($stmt = mysqli_prepare($link, $sql)){
	mysqli_stmt_bind_param($stmt, "ssssssi", $response[0], $response[1], $response[2], $response[3], $response[4], $blacklist, $id);
	// Attempt to execute the prepared statement
	if(!mysqli_stmt_execute($stmt)) {
		echo "Oops! Something went wrong. Please try again later.";
	}
}
mysqli_stmt_close($stmt);

?>