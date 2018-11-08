<?php

session_start();
 
// If session variable is not set it will redirect to login page
if(!isset($_SESSION['username']) || empty($_SESSION['username'])){
  header("location: /login.php");
  exit;
}

require_once realpath("/usr/local/nginx/sql_config.php");

$id = $_SESSION["id"];

$sql = "SELECT `1`,`2`,`3`,`4`,`5`,blacklist FROM config WHERE id = ?";

if($stmt = mysqli_prepare($link, $sql)) {
	mysqli_stmt_bind_param($stmt, "i", $id);
	// Attempt to execute the prepared statement
	if(mysqli_stmt_execute($stmt)) {
		mysqli_stmt_store_result($stmt);
		if(mysqli_stmt_num_rows($stmt) > 0){
			// Bind result variables
			$result = array();
			mysqli_stmt_bind_result($stmt, $result[0], $result[1], $result[2], $result[3], $result[4], $result[5]);
		
			if(mysqli_stmt_fetch($stmt)){
				for ($i=0; $i < count($result)-1; $i++) {
					if ($result[$i] != "") {
						$tmp[] = explode("|", $result[$i]);
					}
				}
				$obj = new stdClass();
				$obj->index = $tmp;
				$obj->blacklist = explode("|", $result[5]);
				echo json_encode($obj);
			}

		} else {
			echo "[]";
		}
	} else{
		echo "Oops! Something went wrong. Please try again later.";
	}
}

mysqli_close($link);

?>