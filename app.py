
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify

import builders

app = Flask(__name__)

from local_dev_help.scripts import consolelog #allows for display to foreman console
app.config["DEBUG"] = True



if 'SECRET_KEY' in os.environ:
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
else:
    app.config['SECRET_KEY'] = 'this_should_be_configured'


###
# Routing
###

@app.route('/')
def index():
    '''
    Make the front page
    '''
    return render_template('index.html', 
                            title="ABD BLDGS - Start"
                            )


@app.route('/abds')
def list_of_abandoned_bldgs():
    '''
    URL to access a JSON list of abandoned buildings
    '''
    abd_bldg_data = builders.abandoned_buildings.list_all()
    abd_bldg_response = jsonify(abd_bldg_data)
    return abd_bldg_response


@app.route('/detail/<address>')
def detail(address):
    '''
    URL to access a list of amenities within .6 miles of an address
    '''
    amn_data = builders.amenities.get_match(address)
    amn_response = jsonify(amn_data)        

    return amn_response


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response

'''
@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
'''

if __name__ == '__main__':
    app.run()
