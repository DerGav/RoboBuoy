//JAVASCRIPT file for RoboBuoy web user interface
//gets data from RoboBuoy and displays it on the page
//will in future also send commands to RoboBuoy

var target_destinations = [];
var target_destinations_with_groups = {};

$(document).ready(function () { // execute as soon as page (=document) is loaded

  $.getJSON($SCRIPT_ROOT + '/send_targetDestinations', // get data from this URL
            //  and execute this function when data arrives
            function(data) //data is now the response from the server
            {
              console.log(data);
              add_targetDestinations(data);
            });

  //call function passed as first parameter over and over again
  //in a set interval of milliseconds
  setInterval( function()
  {
    $.getJSON($SCRIPT_ROOT + '/some_value', // get data from this URL
              //  and execute this function when data arrives
              function(data) //data is now the response from the server
              {
                //console.log(data)
                $('#values').empty(); //remove the data from previous call

                /*
                 * loop through all data pairs and add them to the table
                 * with id 'values' in index.html
                 */
                for( var key in data)
                {  //create new row in table
                  $('<tr></tr>').append($('<th></th>').html(key))
                                .append($('<td></td>').html(data[key]))
                                .appendTo('#values'); //add row to table
                }
              });
  },250); //interval in milliseconds after which to get new data from roboBuoy

  //react to a 'change' of the switch and send according command to roboBuoy
  $('#stopStart').on('change', function (){
    sendCommandToRoboBuoy({
      'motors': $(this).val()
    });

    // ask the server to send us what he received_data
    // this is just done for debugging puproses during development
    get_received_data();
  });

  $('#cancel_add_target').on('click', function() {
    //reset form fields to defaults
    $('#new_target_form')[0].reset();
  });

  $('input:radio[name=new_or_existing_group]').on('change', function () {
    console.log($(this).val());
    if($(this).val() === 'existing_group')
    {
      $('#new_group_name').textinput('disable');
      $('#select_group').selectmenu('enable')
                        .focus();

    }
    else {
      $('#select_group').selectmenu('disable');
      $('#new_group_name').textinput('enable')
                          .focus();
    }
  });

  $('#save_new_target').on('click', updateTargets);

  // react to a 'change' of the target selector
  // and send new location to roboBuoy
  $('#targets').on('change', function () {
    sendCommandToRoboBuoy({
        'set_new_target' : target_destinations[$(this).val()]
    });
    get_received_data();
  });

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

});

//send commands to roboBuoy using AJAX
//use 'receiveCommand' end point of roboBuoys webserver
function sendCommandToRoboBuoy(command)
{
  $.ajax({
            url: $SCRIPT_ROOT + '/receive_command',

            //$('#switch') gets 'form' element which contains the on/off switch
            //the serialize functions translates it so python can understand it
            //data: $('#switch').serialize(),
            data: command,
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

//adds the targets passed in 'targets' array to the webpage's UI
//also stores the targets array in a global variable for easy access
function add_targetDestinations(targets)
{
  //store index that coordinates will have in target_destinations array
  var target_destinations_index = 0;
  target_destinations_with_groups = targets;

  //loop through the targets array
  for (var i=0; i < targets.length; i++)
  {
        //create an html tag for the group and give it a name
        var $select_group = $('<optgroup></optgroup>').attr('label',targets[i].group_name);
        var $list_group = $('<ul data-role="listview" data-filter="true" data-filter-theme="a" data-divider-theme="b"></ul>');
        var $list_group_container = $('<div></div>')
                                        .attr('data-role','collapsible')
                                        .append(
                                          $('<h2></h2>').html(targets[i].group_name)
                                        );

        //loop through the coordinate objects of a group of targets
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
            $('<li></li>').append($('<a></a>')).html(targets[i].coordinates[j].target_name)
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
    }
  }

  console.log(target_destinations);
  console.log(target_destinations_with_groups);

  // reset all form fields to defaults
  $('#new_target_form')[0].reset();
}
