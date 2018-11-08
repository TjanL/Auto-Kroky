<?php

session_start();
 
// If session variable is not set it will redirect to login page
if(!isset($_SESSION['username']) || empty($_SESSION['username'])){
  header("location: /login.php");
  exit;
}

require_once realpath("/usr/local/nginx/sql_config.php");

$id = $_SESSION["id"];

$sql = "SELECT DATE_FORMAT(weekStart,'%d.%m.%Y'),DATE_FORMAT(weekEnd,'%d.%m.%Y'),DATE_FORMAT(updated_at,'%T %d.%m.%Y'),mon,tue,wed,thr,fri FROM log WHERE id = ?";

if($stmt = mysqli_prepare($link, $sql)) {
	mysqli_stmt_bind_param($stmt, "i", $id);
	// Attempt to execute the prepared statement
	if(mysqli_stmt_execute($stmt)) {
		mysqli_stmt_store_result($stmt);
		if(mysqli_stmt_num_rows($stmt) > 0){
			$result = array();
			mysqli_stmt_bind_result($stmt, $weekStart, $weekEnd, $updated, $result[0], $result[1], $result[2], $result[3], $result[4]);
			
			if(mysqli_stmt_fetch($stmt)){
				$obj = new stdClass();
				$obj->weekStart = $weekStart;
				$obj->weekEnd = $weekEnd;
				$obj->updated = $updated;
				$obj->log = $result;
				echo json_encode($obj);
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