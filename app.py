
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
                            title="HVIAB - Start"
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
    Make the detail page, this is going to use legacy code from the hackathon
    for now, eventually the amenities should be served as a json request just
    like the abandoned buildings
    '''
    import csv

    am_full_data = []


    with open('./data_src/amenities.csv', 'rb') as csvfile:
        amreader = csv.reader(csvfile)
        for row in amreader:
            am_full_data.append(row)

    page_data = {}
    am_match_data = []

    #print am_full_data

    for am_row in am_full_data:
        
        if address == am_row[0]:

            page_data["ab_bldg"] = {}

            page_data["ab_bldg"]["adr"] = am_row[1]
            page_data["ab_bldg"]["lat"] = am_row[2]
            page_data["ab_bldg"]["lon"] = am_row[3]

            if float(am_row[10]) < .75:
                am_entry = {}
                am_entry["type"] = am_row[4]
                am_entry["am_name"] = am_row[5]
                am_entry["am_full_adr"] = am_row[6]
                am_entry["dist_to_am"] = am_row[10]
                am_entry["lat"] = am_row[8]
                am_entry["lon"] = am_row[9]

                am_match_data.append(am_entry)

            page_data["matches"] = am_match_data

            page_data["match_count"] = len(am_match_data)

            print page_data

    return render_template("detail.html",
                            am_data=page_data,
                            title="HVIAB - detail")


@app.route('/amns/<address>')
def list_of_nearby_amenities(address):
    '''
    URL to access a list of amenities within .6 miles of an address

    not used in the app yet, falling back to the detail method above
    eventually detail will be deprecated and the json-type interaction
    pattern like on the index page will be used for the amenity details
    as well
    '''
    amn_data = builders.amenities.get_match(address)
    amn_response = jsonify(amn_data)        
    return amn_response


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', title="HVIAB - About")


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


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
