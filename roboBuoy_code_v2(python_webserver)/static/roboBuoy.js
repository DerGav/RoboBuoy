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

  $('#stopStart').on('change', function (){
    sendCommandToRoboBuoy(this.value);

    // ask th server to send us what he received_data
    // this is just done for debugging puproses during development
    $.getJSON($SCRIPT_ROOT + '/show_received', // get data from this URL
              //  and execute this function when data arrives
              function(data) //data is now the response from the server
              {
                console.log(data);
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
            data: $('#switch').serialize(),

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
        var $group = $('<optgroup></optgroup>').attr('label',targets[i].group_name);

        //loop through the coordinate objects of a group of targets
        for(var j=0; j < targets[i].coordinates.length; j++)
        {
          //append a new option to the select group
          $group.append(
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

          //add the coordinate object to global array
          target_destinations[target_destinations_index] = targets[i].coordinates[j];

          //incremenet index so next coordinate obj will be saved to next slot of array
          target_destinations_index++;
        }

        //append the group of options to the select tag ('dropdown menu')
        $group.appendTo('#targets');
  }
  // log array to verify everything went right
  console.log(target_destinations);
}
