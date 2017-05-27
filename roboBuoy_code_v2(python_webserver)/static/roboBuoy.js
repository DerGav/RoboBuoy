//JAVASCRIPT file for RoboBuoy web user interface
//gets data from RoboBuoy and displays it on the page
//will in future also send commands to RoboBuoy

var target_destinations = [];
var target_destinations_with_groups = {};

////////////////////////////////////////////////////////////////////////////////
// Execute as soon as page (=document) is loaded
////////////////////////////////////////////////////////////////////////////////
$(document).ready(function () {

////////////////////////////////////////////////////////////////////////////////
  // Load data from server
////////////////////////////////////////////////////////////////////////////////
  $.getJSON($SCRIPT_ROOT + '/send_targetDestinations', // get data from this URL
			// and execute this function when data arrives
			function(data) // data is now the response from the server
			{
			  console.log(data);
			  add_targetDestinations(data);
			});

  // call function passed as first parameter over and over again
  // in a set interval of milliseconds
  setInterval( function()
  {
	$.getJSON($SCRIPT_ROOT + '/some_value', // get data from this URL
			  // and execute this function when data arrives
			  function(data) // data is now the response from the server
			  {
				console.log("data",data);

				$('#current_lat').html(data.current_lat);
				$('#current_long').html(data.current_long);
				$('#satellites_used').html(data.satellites_used);
				$('#target_lat').html(data.target_lat);
				$('#target_long').html(data.target_long);
				$('#distance_to_target').html(data.distance_to_target);
				$('#speed').html(data.speed);

				update_compass(data.mag_heading);
				update_turn_direction(data.turn_direction);
				update_leak(data.leak);
				update_battery_display(data.battery_voltage);
			  });
  },250); // interval in milliseconds after which to get new data from roboBuoy

////////////////////////////////////////////////////////////////////////////////
  // Setup 'Eventhandlers'
  // ==> determine what happens when user clicks buttons/interacts with page
////////////////////////////////////////////////////////////////////////////////

  // react to a 'change' of the switch and send according command to roboBuoy
  $('#roboBuoy_stopStart').on('change', function (){

	  sendCommandToRoboBuoy('start_stop_roboBuoy', $(this).val() );
	  // ask the server to send us what he received_data
	  // this is just done for debugging puproses during development
	  get_received_data();

  });

  // react to a 'change' of the switch and send according command to roboBuoy
  $('#thrusters_stopStart').on('change', function (){
   sendCommandToRoboBuoy('start_stop_thrusters',$(this).val());
   // ask the server to send us what he received_data
   // this is just done for debugging puproses during development
	get_received_data();
  });

  // react to a 'change' of the switch and send according command to roboBuoy
  $('#shutdown').on('click', function (){
   sendCommandToRoboBuoy('shutdown', 'now');
   // ask the server to send us what he received_data
   // this is just done for debugging puproses during development
   get_received_data();
  });

  // react to a 'change' of the target selector
  // and send new location to roboBuoy
  $('#targets').on('change', function () {
	sendCommandToRoboBuoy('set_new_target',target_destinations[$(this).val()]);
	get_received_data();
  });

  //////////////////////////////////////////////////////////////////////////////
  // setup the 'Add Target...' Dialog
  //////////////////////////////////////////////////////////////////////////////

  // following code block ensures that the new_group_name textinput will be
  // disabled when the add target dialog is opened
  $( "#new_group_name" ).textinput({
	// call this function when the textinput is created/initialized by jQuery
	create: function( event, ui ) {
	  // give tag an arbitrary attribute to tell us that it has been initialized
	  $(this).attr('data-initialized','true');
	}
  });
  $( "#select_group" ).selectmenu({
	// call this function when the textinput is created/initialized by jQuery
	create: function( event, ui ) {
	  // give tag an arbitrary attribute to tell us that it has been initialized
	  $(this).attr('data-initialized','true');
	}
  });
  // call function whenever the add target dialog is opened
  $("a[href='#addTarget']").on('click', function () {
	// pre load the group name textinput
	var $new_group_name = $('#new_group_name');
	var $select_group   = $('#select_group');
	// check if textinput has been initialized
	if( $new_group_name.attr('data-initialized') &&
		$select_group.attr('data-initialized')       )
	{
	  // if so disable it and enable the group selectmenu
	  $new_group_name.textinput('disable');
	  $('#select_group').selectmenu('enable');
	}
  });

  // reset the form when cancel button is clicked
  $('#cancel_add_target').on('click', function() {
	//reset form fields to defaults
	$('#new_target_form')[0].reset();
  });

  // enable/disable the group select and name input depending on user selection
  $('input:radio[name=new_or_existing_group]').on('change', function () {
	//console.log($(this).val());
	// if add to existing group is selected..
	if($(this).val() === 'existing_group')
	{
	  //disable textinput and enable select
	  $('#new_group_name').textinput('disable');
	  $('#select_group').selectmenu('enable')
						.focus(); // puts cursor here
	}
	else {
	  $('#select_group').selectmenu('disable');
	  $('#new_group_name').textinput('enable')
						  .focus(); // puts cursor in the textinput field
	}
  });

  // call updateTargets when the save button is clicked
  $('#save_new_target').on('click', function(){
	  updateTargets();
	  sendCommandToRoboBuoy('save_targets',target_destinations_with_groups);
	  console.log('here');
  });

  //////////////////////////////////////////////////////////////////////////////
  // setup the 'Edit Targets...' Dialog
  //////////////////////////////////////////////////////////////////////////////

  //create a new target group if the button is clicked
  $('#createGroup').on('click', function (){
	// create some html for our new group
	var $new_group = $(' <div data-role="collapsible">').append(
	  $('<h2></h2>').append(
	  $('<input type="text" id="new_group_name" value="enter group name"/>')
	));

	//append html to the collapsibleset on the page
	$('#edit_targets_list').append($new_group)
						   //refresh necessary for changes to take effect
						   .collapsibleset( "refresh" );

	//disable the button, no point in creating a bunch of groups at once
	$(this).attr('disabled','disabled');

	//confirm new group when enter key is pressed
	$('#new_group_name').on('keypress', function (e) {
		 //'e' is the event triggered by keypress
		 // 13 is a code for the enter key
		 if(e.which === 13){
			//Disable textbox to prevent multiple submit
			$(this).attr('disabled');
			//add the text from input field as header for the collapsibleset
			$new_group.find('a').append($('#new_group_name').val());
			//remove the text input
			$new_group.find('input').remove();
			//re enable the button
			$('#createGroup').removeAttr('disabled');
		 }
	});
  });

  init_compass();


});

////////////////////////////////////////////////////////////////////////////////
// Functions
////////////////////////////////////////////////////////////////////////////////

// send 'command' to roboBuoy using AJAX
// using 'receiveCommand' end point of roboBuoys webserver
// for list of commands and their format, refer to documentation
function sendCommandToRoboBuoy(command, values)
{
  $.ajax({
			url: $SCRIPT_ROOT + '/receive_command',
			//data object to send
			data: {
				'command': command,
				'values': values
			},
			//this time we're posting to the server
			type: 'POST',

			//log the servers response or error message to the browser's console
			success: function(response) {
				console.log(response);
			},
			error: function(error) {
				console.log(error);
			}
		});
}

// adds the targets passed in 'targets' array to the webpage's UI
// also stores the targets array in a global variable for easy access
function add_targetDestinations(targets)
{
  // store index that coordinates will have in target_destinations array
  var target_destinations_index = 0;
  target_destinations_with_groups = targets;

  // loop through the targets array
  for (var i=0; i < targets.length; i++)
  {
		// create an html tag for the group and give it a name
		var $select_group = $('<optgroup></optgroup>').attr('label',targets[i].group_name);
		var $list_group = $('<ul data-role="listview" data-filter="true" data-filter-theme="a" data-divider-theme="b"></ul>');
		var $list_group_container = $('<div></div>')
										.attr('data-role','collapsible')
										.append(
										  $('<h2></h2>').html(targets[i].group_name)
										);

		// loop through the coordinate objects of a group of targets
		for(var j=0; j < targets[i].coordinates.length; j++)
		{
		  //append a new option to the select group
		  $select_group.append(
			//create a new html tag for the select option
			// value:
			//   Sets the value that the select tag will take on if this option
			//   is selected. Set to our stored index so we can access
			//   coordinates via global target_destinations array.
			// html:
			//   Sets text between tags.
			//   Here this means the text that will displayed in the dropdown.
			$('<option></option>').attr('value', target_destinations_index)
								  .html(targets[i].coordinates[j].target_name)

		  );
		  $list_group.append(
			$('<li></li>').append($('<a></a>'))
						  .html(targets[i].coordinates[j].target_name)
		  );

		  //add the coordinate object to global array
		  target_destinations[target_destinations_index] = targets[i].coordinates[j];

		  //incremenet index so next coordinate obj will be saved to next slot of array
		  target_destinations_index++;
		}

		//append the group of options to the select tag ('dropdown menu')
		$select_group.appendTo('#targets');
		$list_group_container.append($list_group);
		$list_group_container.appendTo('#edit_targets_list');

		// add the group to the dropdown in the add target dialog
		$('#select_group').append(
		  $('<option></option>').html(targets[i].group_name)
		);
  }
  // log array to verify everything went right
  console.log(target_destinations);
}

// ask the server to send us what he received_data
// this is just done for debugging puproses during development
function get_received_data()
{
  $.getJSON($SCRIPT_ROOT + '/show_received', // get data from this URL
			//  and execute this function when data arrives
			function(data) //data is now the response from the server
			{
			  // just log data to console so we can see it
			  console.log(data);
			});
}

function updateTargets()
{
  // read values from form
  var name  = $('#location_name').val();
  var lat   = $('#location_lat' ).val();
  var long  = $('#location_long').val();

  // user can set the group in 2 different ways so this is more complicated
  var group;

  // get the value of the 'radio' select form element
  var existing_group = $('input:radio[name=new_or_existing_group]:checked').val();
  // set variable depending on value
  if(existing_group === 'existing_group')
  {
	// remember js has no typ binding, so this may look weird but it works!
	existing_group = true;
  } else {
	existing_group = false;
  }

  // if we're adding to an existing group do this...
  if(existing_group)
  {
	// set group to the value selected by the select element
	group = $('#select_group').val();

	//check to see that a real value was selected
	if(group === 'Choose Group...')
	{
	  console.log('No Group Selected!');
	  // TODO: throw an error here or write sth to the UI
	  // console log not good enough
	}
  }
  // if we're creating a new group..
  else {
	//simply get the value of the new group name input field
	group = $('#new_group_name').val();
  }

  // check if values were entered and are valid
  // TODO: add sanity checks here, possibly check for duplicates as well...
  if(name && lat && long && group)
  {
	// create new target object
	var new_target = {
	  target_name: name,
	  Lat: lat,
	  Long: long
	};

	// load the target select UI element, we'll need it a few times
	// no need to let jquery look for it again and again!
	var $targets = $('#targets');

	// are we adding to a group?
	if(existing_group)
	{
	  // need this to calculate index in the quick access array
	  var array_index = 0;

	  // add new target to the saving array
	  // loop through saving array to find the righ spot
	  for(var i=0; i < target_destinations_with_groups.length; i++)
	  {
		// add amount of coordinates per group to array_index, because
		// they are all in one sequence in the quick access array
		array_index += target_destinations_with_groups[i].coordinates.length;

		// check if this is our group
		if(target_destinations_with_groups[i].group_name === group)
		{
		  // add the new target object at the end of the saving array
		  target_destinations_with_groups[i].coordinates.push(new_target);
		  break;
		}
	  }

	  // insert new target into the quick acces array
	  target_destinations.splice(array_index, 0, new_target);

	  // add new target to UI

	  // store if we have already inserted new element
	  var inserted = false;
	  //loop over all groups
	  $.each($targets.find('optgroup'), function () {

		if(inserted) // if we have already inserted the new target..
		{
		  //update the 'value' to resemble the index in the quick acces array
		  $.each($(this).find('option'), function () {
			// ++variable increments the variable before it is evaluated
			// so we set 'value' to 'array_index + 1'
			$(this).attr('value', ++array_index);
		  });
		}
		// if we haven't inserted new target yet work on that
		else {
		  // if the optgroup label equals 'group' that's were we have to insert
		  if ($(this).attr('label') === group)
		  {
			// append the new option in this group
			$(this).append(
			  $('<option></option>').attr('value',array_index)
									.html(name)
			);
			// set the flag to to true because now we have inserted the target
			inserted = true;
		  }
		}
	  });
	}
	// if we're creating a new group as well, do this...
	else {
	  // add new target to the end of the saving array
	  target_destinations_with_groups.push({
		group_name: group,
		coordinates: [new_target]
	  });

	  // add new target to the UI
	  // in this case we can just append the group and the new target
	  $targets.append(
		$('<optgroup></optgroup>').attr('label', group)
								  .append(
									$('<option></option>').attr('value', target_destinations.length)
														  .html(name)
								  )
	  );

	  // add the new target to the quick acces array
	  target_destinations.push(new_target);

	  // add the new group to the dropdown in this dialog
	  $('#select_group').append(
		$('<option></option>').html(group)
	  );


	}
  }

  // log our arrays to see if everything worked
  //console.log(target_destinations);
  //console.log(target_destinations_with_groups);

  // reset all form fields to defaults
  $('#new_target_form')[0].reset();
}

////////////////////////////////////////////////////////////////////////////////
// Battery Display
////////////////////////////////////////////////////////////////////////////////

function update_battery_display(battery_voltage)
{
	//define constants - adapt to batteries being used
	var fully_charged = 16.8;
	var low_voltage   = 14.0;
	//calculate battery percentage
	var percentage = (battery_voltage - low_voltage)/(fully_charged - low_voltage) *100;
	//interpolate between colors
	var color_hue  = (percentage * 1.2).toString();
	var color      = "hsl(" + color_hue + ",100%,50%)";
	//determine width of battery charge bar corresponidng to percantage
	var size = percentage * 1.6;
	//console.log(size);
	//apply the changes
	$('#battery').css('background-color', color)
				 .css('width',size);
}

////////////////////////////////////////////////////////////////////////////////
// Compass
////////////////////////////////////////////////////////////////////////////////
// Global variable
var img = null,
	needle = null,
	ctx = null,
	degrees = 270;

function update_compass(mag_heading)
{
	//update global degrees variable which is used by the compass functions
	// to position the needle
	degrees = mag_heading;
	//add text to page
	$('#mag_heading_txt').html(mag_heading);
}

function clearCanvas() {
	 // clear canvas
	ctx.clearRect(0, 0, 200, 200);
}

function draw() {

	clearCanvas();

	// Draw the compass onto the canvas
	ctx.drawImage(img, 0, 0);

	// Save the current drawing state
	ctx.save();

	// Now move across and down half the
	ctx.translate(100, 100);

	// Rotate around this point
	ctx.rotate(degrees * (Math.PI / 180));

	// Draw the image back and up
	ctx.drawImage(needle, -100, -100);

	// Restore the previous drawing state
	ctx.restore();

	// Increment the angle of the needle by 5 degrees
	//degrees += 5;
}

function imgLoaded() {
	// Image loaded event complete.  Start the timer
	setInterval(draw, 100);
}

function init_compass() {
	console.log("init");
	// Grab the compass element
	var canvas = document.getElementById('compass');

	// Canvas supported?
	if (canvas.getContext('2d')) {
		ctx = canvas.getContext('2d');

		// Load the needle image
		needle = new Image();
		needle.src = 'static/img/modern_needle.png';

		// Load the compass image
		img = new Image();
		img.src = 'static/img/modern_compass.png';
		img.onload = imgLoaded;

		console.log("ctx",ctx,'Img',img,'needle',needle,'deg',degrees);
	} else {
		alert("Canvas not supported!");
	}
}

//turn direction displays
function update_turn_direction(turn_direction)
{
	//toggle between image of arrow poining left and right depending on input
	if(turn_direction == 'left')
	{
		$('#turn_dir').attr('src','static/img/arrow_left.png');
		$('#turn_dir_txt').html('left');
	}
	if(turn_direction == 'right')
	{
		$('#turn_dir').attr('src','static/img/arrow_right.png');
		$('#turn_dir_txt').html('right');
	}
}

//leak displays
function update_leak(leak)
{
	//toggle between images to signify leak or no leak depending on input
	if(leak)
	{
		$('#leak_txt').html('LEAK DETECTED');
		$('#leak').attr('src','static/img/leak_detected.png');
	}
	else {
		$('#leak_txt').html('No Leaks');
		$('#leak').attr('src','static/img/leak_grayed.png');
	}
}
