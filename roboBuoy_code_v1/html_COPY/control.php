<?php
  $t = time();
  $timestamp = date("Y-m-d h:m:s", $t);
  $robocolor = 'white';
  $mcolor = 'green';
  $message = "No current messages.";
  $target_choice = "";
  // This array contains the locations we want to have readily available.
  // These values should be referenced from here, not typed elsewhere in the code.
  // For example $targets[1][2] is the longitude of the item in the second row.
  // NOTE: php arrays count from zero!
  $targets = array (
	array('North side of CSUMB pool', 36.651503, -121.807078),
        array('South side of CSUMB pool', 36.651364, -121.807128),
	array('Squid Mops', 36.36621, -121.53171),
	array('Sand Dollar Bed', 36.623883, -121.907348),
        array('Near intake pipe(bogus values)', 36.0, -121.0),
        array('Carmel River Canyon', 36.535028, -121.938936),
	array('DESAL - A', 36.615505,-121.894724),
	array('DESAL - B', 36.615785,-121.894876),
	array('DESAL - C', 36.616061,-121.895023),
	array('DESAL - D', 36.616301,-121.895218),
	array('DESAL - E', 36.616558,-121.895371)
  );
	
  if( isset($_GET["color"]) ) {
      $robocolor = $_GET['color'];
  }
//Stop Button
  if (isset($_POST["StopCommand"])) {
      $flagfile = fopen("/home/pi/data_to_buoy/stop.txt", "w") or die ("Unable to open stop file!");
      fclose($flagfile);
      $message = "Sent stop command to RoboBuoy";
      $mcolor = "green";
//Go Button
 } else if (isset($_POST["GoCommand"])) {
	$flagfile = fopen("/home/pi/data_to_buoy/go.txt", "w") or die ("Unable to open go file!");
	fclose($flagfile);
	$messege = "Sent go command to RoboBuoy";
	$mcolor = "green";
//Reset Button
} else if (isset($_POST["Reset"])) {
	$flagfile = fopen ("/home/pi/data_to_buoy/reset.txt", "w") or die ("Unable to open reset file");
	fclose($flagfile);
	$messege = "Sent reset command to RoboBuoy";
	$mcolor = "green";
  } else if (isset($_POST["SetHome"])) {
      $flagfile = fopen("/home/pi/data_to_buoy/set_home.txt", "w") or die ("Unable to open set location file!");
      $message = "Asked RoboBuoy to set new home location.";
      $mcolor = "green";
      fclose($flagfile);
  } else if (isset($_POST["StartScriptCommand"])) {
      $flagfile = fopen("/home/pi/data_to_buoy/startScripts.txt", "w") or die ("Unable to open startScripts file!");
      $message = "Asked RoboBuoy to start control software.";
      $mcolor = "green";
      fclose($flagfile);
  } else if (isset($_POST["RestartScriptCommand"])) {
      $flagfile = fopen("/home/pi/data_to_buoy/restartScripts.txt", "w") or die ("Unable to open restartScripts file!");
      $message = "Asked RoboBuoy to restart control software.";
      $mcolor = "green";
      fclose($flagfile);
  } else if (isset($_POST["StopScriptCommand"])) {
      $flagfile = fopen("/home/pi/data_to_buoy/stopScripts.txt", "w") or die ("Unable to open stopScripts file!");
      $message = "Asked RoboBuoy to stop control software.";
      $mcolor = "orange";
      fclose($flagfile);
  } else if (isset($_GET["targets"])) {
      $target_choice=$_GET["targets"];
      //$flagfile = fopen("data_to/target_location.txt", "w") or die ("Shark attack! AHHH!");
      $flagfile = fopen("/home/pi/data_to_buoy/target_location.txt", "w") or die ("Shark attack! AHHH!");

      $message = "Set destination to RoboBuoy.";
      $mcolor = "green";

      if ($target_choice != "" && $target_choice < count($targets)) {
	$Lat  = $targets[$target_choice][1];
	$Long = $targets[$target_choice][2];
	$message = "Set destination to " . $targets[$target_choice][0] . "<br>";
        $mcolor = "green";
      } else {
         $message = "Something's wrong, location not recognized.";
         $mcolor = "red";
      } 
      fwrite($flagfile,$Lat);
      fwrite($flagfile,"\n");
      fwrite($flagfile,$Long);
      fwrite($flagfile,"\n");
      fclose($flagfile);
  }

/*
$Currentlocation="";
$GPS = fopen("/home/pi/GPS.txt", "r") or die ("Unable to open file!");
while(!feof($GPS))
{
// the dot means concatenates the two items together
	$Currentlocation = $Currentlocation . fgets($GPS);
}
fclose($GPS);
 */

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
    <title>Robo Buoy Detailed Control</title>
  </head>
  <body style="background-color:<?= $robocolor ?>">
    <div class="main_page">
      <div class="buoy_data">
	<?= $timestamp ?><br>
	<br><span style="font-size: 14pt">Warning: This page does not auto-update.  <a href="index.php">Take me to the Status Page</a></span>
	<br><span style="color: <?= $mcolor ?>; font-size: 16pt"><?= $message ?></span>

	<form method="POST" >
	<br><br>
	<input value="Stop!" id="stopcommand" name="StopCommand" type="submit">
	<br><br>
	<input value="Go!" id="gocommand" name="GoCommand" type="submit">
	<br><br>
	<input value="Reset" id="reset" name="Reset" type="submit">
	<input value="Set New Home" id="sethome" name="SetHome" type="submit">
	</form>
	<br><br>
	<form method="GET">
	<select name="targets">
<?php
	for ($i = 0; $i < count($targets); $i++) {
	  $name = $targets[$i][0];
	  if ($target_choice == $i) $sel = ' selected="selected"'; 
  	  else $sel = "";
	  echo "<option value=\"$i\" $sel >$name</option>";
        }
 ?>
          <input value="Set Destination" id="setcommand" name="setcommand" type="submit">
        </form>
	<table>
	<tr><th>Item</th><th>Value</th></tr>
        <?= $buoyLines ?>
	<!--
	<tr><td>Battery</td><td>78%</td></tr>
	<tr><td>Target Name</td><td>Carmel River Canyon</td></tr>
	<tr><td>Target Location</td><td>
	 -->

	</table>

	 <table>
        <tr><th>Speed</th><th>Value desired</th></tr>
	<tr><td>KP </td><td><input type="text" value="TBD" name="KP_Speed_Box"></td><tr>
	<tr><td>KI </td><td>add textbox here</td><tr>
	<tr><td>KD </td><td>add textbox here</td><tr>
	</table>

	<table> 
	<tr><th>Heading</th><th>Value desired</th></tr>
	<tr><td>KP </td><td>add textbox here</td><tr>
	<tr><td>KI </td><td>add textbox  here</td><tr>
	<tr><td>KD </td><td>add textbox here</td><tr>
	</table>
      </div>
      <div class="extras">
	<br><br>
	<form method="GET">
	<select name="color">
	  <option value="aqua"<?php if ($robocolor == 'aqua') echo '  selected="selected"'; ?>>Aqua</option>
	  <option value="aquamarine"<?php if ($robocolor == 'aquamarine') echo '  selected="selected"'; ?>>Aquamarine</option>
	  <option value="mediumaquamarine"<?php if ($robocolor == 'mediumaquamarine') echo '  selected="selected"'; ?>>Medium Aquamarine</option>
	  <option value="coral"<?php if ($robocolor == 'coral') echo '  selected="selected"'; ?>>Coral</option>
	  <option value="salmon"<?php if ($robocolor == 'salmon') echo '  selected="selected"'; ?>>Salmon</option>
	  <option value="seashell"<?php if ($robocolor == 'seashell') echo '  selected="selected"'; ?>>Seashell</option>
	  <option value="white"<?php if ($robocolor == 'white') echo '  selected="selected"'; ?>>White</option>
	</select>
	<br>
	<input value="Set Color" id="setcommand" name="setcommand" type="submit">
	</form>
	<br>
      </div>
    </div>
    <div>
	These controls are for stopping and starting all of the control programs.  Normally you will only use them at the beginning of a mission or at the end.  It may also be useful to "Restart" if the software is not responding to other commands.
	<form method="POST" >
	<br><br>
	<input value="Start Voltage Check and Motor Control!" id="startScriptCommand" name="StartScriptCommand" type="submit">
	<br><br>
	<input value="Restart Control Software" id="restartScriptCommand" name="RestartScriptCommand" type="submit">
	<br><br>
	<input value="Stop all Control Programs" id="stopScriptCommand" name="StopScriptCommand" type="submit">
	</form>
    </div>
  </body>
</html>

