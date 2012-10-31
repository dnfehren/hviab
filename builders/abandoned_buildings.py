import csv

from local_dev_help.scripts import consolelog

def list_all():

    v_header = []
    v_data = []

    with open('./data_src/vacants_latest.csv') as vacants_csv:
        v_reader = csv.reader(vacants_csv)

        for row_num, row in enumerate(v_reader):
            if row_num == 0:
                                
                for row_part in row:
                    col_head = {'sTitle':row_part}
                    v_header.append(col_head)

            else:
                row.append(row[19].replace(" ", "_").lower().replace(".",""))
                v_data.append(row)

    head = {'titles':v_header}
    data = {'data':v_data}

    data_container = {"abd_bldgs" : [head, data]} 
    
    return data_container