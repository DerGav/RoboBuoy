#Python script for serving the RoboBuoy control page

# import functions from libraries so we can use them
#   - 'flask' lets our python script act like a webserver
#     we don't need everything so just import a few things from flask
from flask import Flask,render_template,jsonify

#initialize Flask webapp
app = Flask(__name__)

#define global variable used for testing
i = 0

# for a request to the root directory of our webpage call the index() function
@app.route('/')
#define a function (fka Subroutine) called index
def index():
    #render (=translate) the file 'index.html' from the templates directory to
    #real html and return it to the browser that requested it
    return render_template('index.html')

#define what to do for request to '/some_value'
@app.route('/some_value')
def add_numbers():
    # we need to add this line so we can use the global variable i in this function
    # python would otherwise create a new local variable with the same name
    global i;

    #create 'dictionary' and fill it with data pairs (key and value)
    #filled with bogus values right now for testing
    #eventually should be filled with data from RoboBuoy
    data = {
                '2. someValue1': i,
                '1. someValue2': '&#8594; East', # '&#8594;' = code for arrow
                '3. xand another one': 300

            }

    #increment the global(!) variable i to simulate a changing value for testing
    i += 1;

    #This line sends the data to whoever requested it, most likely some browser.
    #Because browsers generally don't speak python the function 'jsonify'
    #takes the python dictionary 'data' and translates it to
    #JavaScriptObjectNotation(JSON) so that it can be processed by a browser.
    return jsonify(data)

#this is pythons way of saying:"start the code execution here" ('main' function)
#detailed explanation:
#   http://ibiblio.org/g2swap/byteofpython/read/module-name.html
if __name__ == '__main__':

    #run the flask webapp we initialized at the top
    # "debug=True" :
    #       run in debug mode (a bit slower, but easier to troubleshoot)
    # "host='0.0.0.0'" :
    #       runs the server on the pi's IP-Adress and so makes it
    #       available to anyone in the same network
    app.run(debug=True, host='0.0.0.0')
