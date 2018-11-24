<?php

session_start();
 
// If session variable is not set it will redirect to login page
if(!isset($_SESSION['username']) || empty($_SESSION['username'])){
  header("location: /login.php");
  exit;
}

require_once realpath("/usr/local/nginx/sql_config.php");

$id = $_SESSION["id"];

$sql = "SELECT updated_at FROM log WHERE id = ?";

if($stmt = mysqli_prepare($link, $sql)) {
	mysqli_stmt_bind_param($stmt, "i", $id);
	// Attempt to execute the prepared statement
	if(mysqli_stmt_execute($stmt)) {
		mysqli_stmt_store_result($stmt);
		if(mysqli_stmt_num_rows($stmt) > 0){
			// Bind result variables
			mysqli_stmt_bind_result($stmt, $updated_at);
		
			if(mysqli_stmt_fetch($stmt)){
				$timeLimit = (15) * 60; // in minutes
				if ((time()-$timeLimit) > strtotime($updated_at)) {
					putenv('LANG=en_US.UTF-8');

					exec("/usr/local/bin/python3 /path/to/file/auto_malica_v5.0_web_single.py " . $id);
				} else {
					echo $timeLimit - (time() - strtotime($updated_at));
				} 
			}
		}
	} else{
		echo "Oops! Something went wrong. Please try again later.";
	}
}
mysqli_stmt_close($stmt);

?>