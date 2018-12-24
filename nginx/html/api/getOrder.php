<?php

session_start();
 
// If session variable is not set it will redirect to login page
if(!isset($_SESSION['username']) || empty($_SESSION['username'])){
  header("location: /login.php");
  exit;
}

require_once realpath("/usr/local/nginx/sql_config.php");
header("Content-type: text/json; charset=utf-8");

$id = $_SESSION["id"];

$sql = "SELECT DATE_FORMAT(week_start,'%d.%m.%Y'),DATE_FORMAT(week_end,'%d.%m.%Y'),DATE_FORMAT(updated_at,'%T %d.%m.%Y'),order_log FROM log WHERE id = ?";

if($stmt = mysqli_prepare($link, $sql)) {
	mysqli_stmt_bind_param($stmt, "i", $id);
	// Attempt to execute the prepared statement
	if(mysqli_stmt_execute($stmt)) {
		mysqli_stmt_store_result($stmt);
		if(mysqli_stmt_num_rows($stmt) > 0){
			mysqli_stmt_bind_result($stmt, $weekStart, $weekEnd, $updated, $log);
			
			if(mysqli_stmt_fetch($stmt)){
				$obj = new stdClass();
				$obj->weekStart = $weekStart;
				$obj->weekEnd = $weekEnd;
				$obj->updated = $updated;
				$obj->log = json_decode($log);
				echo json_encode($obj, JSON_UNESCAPED_UNICODE);
			}
		} else {
			echo "{}";
		}
	} else{
		echo "Oops! Something went wrong. Please try again later.";
	}
}

mysqli_close($link);

?>