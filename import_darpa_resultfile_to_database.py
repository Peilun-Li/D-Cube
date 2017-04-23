from DCube_params import *
from DCube_sql import *
import sys
import os
import glob, os

try:
    db_conn = connect_db()
except:
    print "Error: could not connect to database. Please modify psql account/port information in DCube_params.py to connect to psql"
    exit(-1)

folderpath = sys.argv[1]
os.chdir(folderpath)

for file in glob.glob("*.csv"):

    if 'results' in file:

        if ('ari' not in file) or ('dense' not in file):
            continue

        path = os.path.join(folderpath, file)
        if not os.path.exists(path):
            print "Error: could not find data file. Please modify the data_path parameter in Makefile to the path of darpa.csv (without label)"
            exit(-1)
        path = os.path.abspath(path)

        try:
            print "Copying data..."
            relation = file.split(".")[0]

            if DEBUG:
                print 'relation=', relation
                print 'path=', path

            drop_and_create_table(db_conn, relation, "source varchar(20), destination varchar(20), timestamp varchar(20), label varchar(20), block_idx varchar(20)")
            exec_sql(db_conn, "copy %s(source, destination, timestamp, label, block_idx) from '%s' delimiter ',' CSV HEADER" % (relation, path))
            exec_sql(db_conn, "alter table %s alter column timestamp type varchar(13) using SUBSTR(timestamp, 1, 13)" % relation)

            print "Data '%s' copied to table darpa_sample" % relation
           
        except KeyboardInterrupt:
            print "exit manually"

close_db(db_conn)
exit(0)
