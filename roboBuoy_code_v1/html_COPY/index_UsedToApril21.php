<?php
  $t = time();
  $timestamp = date("Y-m-d h:m:s", $t);
  $robocolor = 'white';
  $message = "";
  if( $_GET["color"] ) {
      $robocolor = $_GET['color'];
  }
  if ($_POST["StopCommand"]) {
      $flagfile = fopen("/home/pi/data_to_buoy/stop.txt", "w") or die ("Unable to open stop file!");
      fclose($flagfile);
      $message = "Sent stop command to RoboBuoy";
      $mcolor = "green";
  } else if ($_POST["SetHome"]) {
      $flagfile = fopen("/home/pi/data_to_buoy/set_home.txt", "w") or die ("Unable to open set location file!");
      $message = "Asked RoboBuoy to set new home location.";
      $mcolor = "green";
      fclose($flagfile);
  } else if ($_GET["targets"]) {
      $target_choice=$_GET["targets"];
      //$flagfile = fopen("data_to/target_location.txt", "w") or die ("Shark attack! AHHH!");
      $flagfile = fopen("/home/pi/data_to_buoy/target_location.txt", "w") or die ("Shark attack! AHHH!");

      $message = "Set destination to RoboBuoy.";
      $mcolor = "green";

      if ($target_choice==1){
         $Lat="36.651503";
         $Long="-121.807078";
      } else if ($target_choice==2){
         $Lat="36.651364";
         $Long="-121.807128";
      } else if ($target_choice==3){
         $Lat="13274902183490213822";
         $Long="13274902183490213822";
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
$buoyOutput = fopen("/home/pi/data_from_buoy/colecode.txt", "r");
if (!buoyOutput) {
    $message .= "<br>ERROR: No new data output from RoboBuoy controller!<br>\n";
    $mcolor = "red";
} else {
    $buoyLines = "";
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
    <meta http-equiv="refresh" content="10"
    <title>Robo Buoy Status and Control</title>
  </head>
  <body style="background-color:<?= $robocolor ?>">
    <div class="main_page">
      <div class="buoy_data">
	<?= $timestamp ?><br>
	Hi.  I'm RoboBuoy.  Things are going fine.
	<br><span style="color: <?= $mcolor ?>; font-size: 16pt"><?= $message ?></span>

	<table>
	<tr><th>Item</th><th>Value</th></tr>
        <?= $buoyLines ?>
	<!--
	<tr><td>Battery</td><td>78%</td></tr>
	<tr><td>Target Name</td><td>Carmel River Canyon</td></tr>
	<tr><td>Target Location</td><td>
	 -->
	<form method="GET">
	<select name="targets">
	  <option value="1"<?php if ($target_choice == '1') echo '  selected="selected"'; ?>>North side of CSUMB pool</option>
	  <option value="2"<?php if ($target_choice == '2') echo ' selected="selected"'; ?>>South side of CSUMB pool</option>
	  <option value="3"<?php if ($target_choice == '3') echo ' selected="selected"'; ?>>Near intake pipe</option>
	  </select>
          <input value="Set Destination" id="setcommand" name="setcommand" type="submit">
        </form>

	<!--
	<tr><td>Current Location</td><td>Current location</td></tr>
	<tr><td>Current Heading</td><td>230 degrees</td></tr>
	<tr><td>Move needed</td><td>5 m at 233 degrees</td></tr>
	<tr><td>Thrust</td><td>80% forward</td></tr>
	<tr><td>Turning </td><td>2% starboard</td></tr>
	<tr><td>Magnetic declination</td><td>+13.3 East</td></tr>
	 -->
	</table>

	<!--
	 <table>
        <tr><th>Speed</th><th>Value desired</th></tr>
	<tr><td>KP </td><td>add textbox here</td><tr>
	<tr><td>KI </td><td>add textbox here</td><tr>
	<tr><td>KD </td><td>add textbox here</td><tr>
	</table>

	<table> 
	<tr><th>Heading</th><th>Value desired</th></tr>
	<tr><td>KP </td><td>add textbox here</td><tr>
	<tr><td>KI </td><td>add textbox  here</td><tr>
	<tr><td>KD </td><td>add textbox here</td><tr>
	</table>
	-->
      </div>
      <div class="buoy_data">
	<br><br>
	You can send me instructions:<br>
	<form method="POST" >
	<select name="targets">
	  <option value="1" selected="selected">Carmel River Canyon</option>
	  <option value="2">CSUMB Pool, Lane 6</option>
	  <option value="3">Great Pacific Gyre</option>
	</select>
	&nbsp;&nbsp;
	<input value="Send new Location" id="newloc" name="NewLoc" type="submit">
	<br><br>
	<input value="Stop!" id="stopcommand" name="StopCommand" type="submit">
	<br><br>
	<input value="Set New Home" id="sethome" name="SetHome" type="submit">
	</form>
    </div>
    <div class="extras">
	<br><br>
	<form>
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
  </body>
</html>

