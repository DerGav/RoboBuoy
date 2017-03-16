//JAVASCRIPT file for RoboBuoy web user interface
//gets data from RoboBuoy and displays it on the page
//will in future also send commands to RoboBuoy

$(document).ready(function () { // execute as soon as page (=document) is loaded

  //call function passed as first parameter over and over again
  //in a set interval of milliseconds
  setInterval( function()
  {
    $.getJSON($SCRIPT_ROOT + '/some_value', // get data from this URL
              //  and execute this function when data arrives
              function(data) //data is now the response from the server
              {
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

});
