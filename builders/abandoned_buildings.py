import csv

from local_dev_help.scripts import consolelog

def list_all():

    v_header = []
    v_data = []

    with open('./data_src/vacants_snap.csv') as vacants_csv:
        v_reader = csv.reader(vacants_csv)

        for row_num, row in enumerate(v_reader):
            if row_num == 0:
                                
                for row_part in row:
                    col_head = {'sTitle':row_part}
                    v_header.append(col_head)

            else:
                row_adr = row.pop(0)
                link_adr = row_adr.replace(" ", "_").lower().replace(".","")
                row.insert(0, '<a href="/detail/' + link_adr + '">' + row_adr + '</a>')
                v_data.append(row)

    head = {'titles':v_header}
    data = {'rows':v_data}

    data_container = {"data" : [head, data]} 
    
    return data_container