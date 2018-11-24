<?php

//The username or email address of the account.
define('USERNAME', 'ljutjan');
 
//The password of the account.
define('PASSWORD', 'lipnbaker');
 
//Set a user agent. This basically tells the server that we are using Chrome ;)
define('USER_AGENT', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36');
 
//Where our cookie information will be stored (needed for authentication).
define('COOKIE_FILE', 'cookie.txt');
 
//URL of the login form.
define('LOGIN_FORM_URL', 'http://www.kroky.si/2016/?mod=register&action=login');
 
//Login action URL. Sometimes, this is the same URL as the login form.
define('LOGIN_ACTION_URL', 'http://www.kroky.si/2016/?mod=register&action=login');
 
 
//An associative array that represents the required form fields.
//You will need to change the keys / index names to match the name of the form
//fields.
$postValues = array(
    'username' => USERNAME,
    'password' => PASSWORD
);
 
//Initiate cURL.
$curl = curl_init();
 
//Set the URL that we want to send our POST request to. In this
//case, it's the action URL of the login form.
curl_setopt($curl, CURLOPT_URL, LOGIN_ACTION_URL);
 
//Tell cURL that we want to carry out a POST request.
curl_setopt($curl, CURLOPT_POST, true);
 
//Set our post fields / date (from the array above).
curl_setopt($curl, CURLOPT_POSTFIELDS, http_build_query($postValues));
 
//We don't want any HTTPS errors.
curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
 
//Where our cookie details are saved. This is typically required
//for authentication, as the session ID is usually saved in the cookie file.
curl_setopt($curl, CURLOPT_COOKIEJAR, COOKIE_FILE);
 
//Sets the user agent. Some websites will attempt to block bot user agents.
//Hence the reason I gave it a Chrome user agent.
curl_setopt($curl, CURLOPT_USERAGENT, USER_AGENT);
 
//Tells cURL to return the output once the request has been executed.
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
 
//Allows us to set the referer header. In this particular case, we are 
//fooling the server into thinking that we were referred by the login form.
curl_setopt($curl, CURLOPT_REFERER, LOGIN_FORM_URL);
 
//Do we want to follow any redirects?
curl_setopt($curl, CURLOPT_FOLLOWLOCATION, false);
 
//Execute the login request.
curl_exec($curl);
 
//Check for errors!
if(curl_errno($curl)){
    throw new Exception(curl_error($curl));
}
 
//We should be logged in by now. Let's attempt to access a password protected page
curl_setopt($curl, CURLOPT_URL, 'http://www.kroky.si/2016/?mod=register&action=order');

curl_setopt($curl, CURLOPT_POST, false);
 
//Use the same cookie file.
curl_setopt($curl, CURLOPT_COOKIEJAR, COOKIE_FILE);
 
//Use the same user agent, just in case it is used by the server for session validation.
curl_setopt($curl, CURLOPT_USERAGENT, USER_AGENT);
 
//We don't want any HTTPS / SSL errors.
curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);

//Execute the GET request and print out the result.
#echo curl_exec($curl);

$meniji = [
	"osnovni topli" => 3,
	"vitalni topli" => 4,
	"vegi topli" => 5,
	"fast topli" => 6,
	"solatni" => 7,
	"osnovni hladni" => 9,
	"vitalni hladni" => 10,
	"vegi hladni" => 11,
	"sweet hladni" => 12,
	"brez s" => 13,
	"dieta topli" => 15,
	"dieta hladni" => 16,
	"žlica meni" => 18,
	"tradicionalni menu" => 19
];

$teden = [
	"pon" => 2,
	"tor" => 3,
	"sre" => 4,
	"cet" => 5,
	"pet" => 6,
	"sob" => 7
];

$html = new DOMDocument();
libxml_use_internal_errors(true);
$html->loadHTML(curl_exec($curl));

$xpath = new DOMXPath($html);
$content_table = $xpath->query("//table[@id='order_table']")->item(0);


function checkItem($day, $menu)
{
	global $xpath, $content_table, $meniji, $teden;

	$item = $xpath->query("tr[{$meniji[$menu]}]/td[{$teden[$day]}]/label/span/span", $content_table)->item(0);
	
	if ($item->textContent != "") {
		return $item->textContent;
	} else {
		return false;
	}
}

function checkXXL($day, $menu)
{
	global $xpath, $content_table, $meniji, $teden;

	$item = $xpath->query("tr[{$meniji[$menu]}]/td[{$teden[$day]}]/div", $content_table)->item(0);
	
	if ($item->getAttribute("style") == "display:block") {
		return true;
	} else {
		return false;
	}
}

function weekDate()
{
	global $xpath, $content_table;

	$mon = $xpath->query("thead/tr/td[2]/span", $content_table)->item(0);
	$fri = $xpath->query("thead/tr/td[6]/span", $content_table)->item(0);
	
	return [trim($mon->textContent, "()"), trim($fri->textContent, "()")];
}

function selectItem($day, $menu)
{
	global $curl, $xpath, $content_table, $meniji, $teden;

	$item = $xpath->query("tr[{$meniji[$menu]}]/td[{$teden[$day]}]/input", $content_table)->item(0);
	$id = $item->getAttribute("cat_id");
	$date = $item->getAttribute("name");

	$data = array('c' => $id, 'date' => $date);
	curl_setopt($curl, CURLOPT_URL, 'http://www.kroky.si/2016/?mod=register&action=user2date2menu');

	curl_setopt($curl, CURLOPT_POST, true);

	curl_setopt($curl, CURLOPT_POSTFIELDS, http_build_query($data));
	 
	//Use the same cookie file.
	curl_setopt($curl, CURLOPT_COOKIEJAR, COOKIE_FILE);
	 
	//Use the same user agent, just in case it is used by the server for session validation.
	curl_setopt($curl, CURLOPT_USERAGENT, USER_AGENT);
	 
	//We don't want any HTTPS / SSL errors.
	curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
	curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);

	curl_setopt($curl, CURLOPT_REFERER, "http://www.kroky.si/2016/?mod=register&action=order");

	curl_exec($curl);

	if(curl_errno($curl)){
    	echo "Could not select the item! $day, $menu";
	}
}

function sendEmail()
{
	global $curl, $xpath, $content_table;

	$mon = $xpath->query("thead/tr/td[2]/span", $content_table)->item(0);
	$sun = $xpath->query("thead/tr/td[7]/span", $content_table)->item(0);

	$data = array('from' => trim($mon->textContent, "()"), 'to' => trim($sun->textContent, "()"));
	curl_setopt($curl, CURLOPT_URL, 'http://www.kroky.si/2016/?mod=register&action=send_order_email');

	curl_setopt($curl, CURLOPT_POST, true);

	curl_setopt($curl, CURLOPT_POSTFIELDS, http_build_query($data));
	 
	//Use the same cookie file.
	curl_setopt($curl, CURLOPT_COOKIEJAR, COOKIE_FILE);
	 
	//Use the same user agent, just in case it is used by the server for session validation.
	curl_setopt($curl, CURLOPT_USERAGENT, USER_AGENT);
	 
	//We don't want any HTTPS / SSL errors.
	curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
	curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);

	curl_setopt($curl, CURLOPT_REFERER, "http://www.kroky.si/2016/?mod=register&action=send_order_email");

	curl_exec($curl);

	if(curl_errno($curl)){
    	echo "Could not send email! " . curl_errno($curl);
	}
}

echo implode(", ", weekDate());
echo "<br>";

echo checkItem("cet", "osnovni topli");
echo "<br>";

#echo checkXXL("cet", "fast topli");
#echo "<br>";

#selectItem("cet","osnovni topli");
#echo "<br>";

#sendEmail();
#echo "<br>";

?>