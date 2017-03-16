<?php
  $refreshSeconds = 3;
  $t = time();
  $timestamp = date("Y-m-d h:m:s", $t);
  $mcolor = 'green';
  $message = "RoboBuoy is happy.";
  $target_choice = "";
  if (isset($_POST["StopCommand"])) {
      $flagfile = fopen("/home/pi/data_to_buoy/stop.txt", "w") or die ("Unable to open stop file!");
      fclose($flagfile);
      $message = "Sent stop command to RoboBuoy";
      $mcolor = "green";
  } else if (isset($_POST["SetHome"])) {
      $flagfile = fopen("/home/pi/data_to_buoy/set_home.txt", "w") or die ("Unable to open set location file!");
      $message = "Asked RoboBuoy to set new home location.<br>";
      $mcolor = "green";
      fclose($flagfile);
# The else block below violates rules against running root code from
# a web server.  Find a better way to start control code from the web?
#  } else if (isset($_POST["StartCode"])) {
#      $shell_msg = shell_exec("/home/pi/robo start 2>&1");
#      print_r($shell_msg);
#      #$message = "Started RoboBuoy voltage monitor and motor control.<br>";
#      $message = $shell_msg;
#      $mcolor = "green";
#      fclose($flagfile);
  }

// Now read an actual file of information from the buoy.  Each line will
// come in with two sets if <td> tags.
//$buoyOutput = fopen("/home/pi/data_from_buoy/colecode.txt", "r") or die ("Unable to open data file from RoboBuoy!");

$buoyLines = "";  // A variable for storing text we get from the control programs
$buoyOutput = fopen("/home/pi/data_from_buoy/colecode.txt", "r");
if (!$buoyOutput) {
    $message .= "<br>ERROR: No new data output from RoboBuoy controller!<br>\n";
    $mcolor = "red";
} else {
    while(!feof($buoyOutput))
    {
	    $buoyLines .= "<tr>" . fgets($buoyOutput) . "</tr>";
    }
}
fclose($buoyOutput);

$leakOutput = fopen("/home/pi/data_from_buoy/leak.txt", "r");
if (!$leakOutput) {
    ; # No leak is a good leak.
} else {
	$message = "Leak video should be here:<video width=\"320\" height=\"240\" autoplay loop>
	$refreshSeconds = 3600
		<source src=\"LeakVideo.mp4\" type=\"video/mp4\">
		Your browser does not support the video tag.
		</video>";

}
fclose($buoyOutput);

$buoyOutput = fopen("/home/pi/data_from_buoy/battery.txt", "r");
if (!$buoyOutput) {
    $message .= "<br>ERROR: No RoboBuoy battery status!<br>\n";
    $mcolor = "red";
} else {
    while(!feof($buoyOutput))
    {
	    $buoyLines .= "<tr>" . fgets($buoyOutput) . "</tr>";
    }
}
fclose($buoyOutput);


?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta http-equiv="refresh" content="<?= $refreshSeconds ?>"
    <title>Robo Buoy Status and Control</title>
  </head>
  <body >
    <div class="main_page">
      <div class="buoy_data">
	<?= $timestamp ?><br>
	<br><span style="color: <?= $mcolor ?>; font-size: 16pt"><?= $message ?></span>

	<table>
	<tr><th>Item</th><th>Value</th></tr>
        <?= $buoyLines ?>
	</table>

      </div>
      <div class="buoy_data">
	<br>
	Basic Controls:<br>
	<form method="POST" >
	<input value="Stop!" id="stopcommand" name="StopCommand" type="submit">
	<br><br>
	<input value="Set New Home" id="sethome" name="SetHome" type="submit">
	</form>
	<br><br>
	<span style="font-size: 18pt">
	<a href="control.php">Detailed Controls</a>
	</span>
      </div>
    </div>
  </body>
</html>

