import csv

from local_dev_help.scripts import consolelog

def get_match(id):
    '''
    not yet used in the app, using old logic from initial hackathon version

    need to figure out how to get json data loaded into page w/o
    full request back to flask/page reload
    '''

    a_data = []

    with open('./data_src/amenities_data.csv') as amenities_csv:
        a_reader = csv.reader(amenities_csv)

        for row_num, row in enumerate(a_reader):
            if row[0] == id:
                a_data.append(row)

    if len(a_data) == 0:
        a_data = 'no-match'

    data = {'data':a_data}

    data_container = {"amenities" : data} 
    
    return data_container