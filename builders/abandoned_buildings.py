import csv

from local_dev_help.scripts import consolelog

def list_all():

    v_data = []

    def make_adr_id(raw_adr):
        adr_id = raw_adr.replace(" ", "_").lower().replace(".","")
        return adr_id

    with open('./data_src/vacants_latest.csv') as vacants_csv:
        v_reader = csv.reader(vacants_csv)

        for row_num, row in enumerate(v_reader):

            out_row = []
            out_row.append(row[19]) #full address
            out_row.append(row[18]) #zip
            out_row.append(row[25]) #lat
            out_row.append(row[26]) #lon
            out_row.append(make_adr_id(row[19]))
            v_data.append(out_row)

    data_container = {'aaData':v_data}
    
    return data_container