//JAVASCRIPT file for RoboBuoy web user interface
//gets data from RoboBuoy and displays it on the page
//will in future also send commands to RoboBuoy

var target_destinations = [];

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
