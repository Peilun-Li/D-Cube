from DCube_params import *
from DCube_sql import *
import sys
import os

path = sys.argv[1]
if not os.path.exists(path):
    print "Error: could not file data file. Please modify the data_path parameter in Makefile to the path of darpa.csv (without label)"
    exit(-1)
path = os.path.abspath(path)

try:
    db_conn = connect_db()
except:
    print "Error: could not connect to database. Please modify psql account/port information in DCube_params.py to connect to psql"
    exit(-1)

print "Copying data..."
drop_and_create_table(db_conn, "darpa_sample", "source varchar(20), destination varchar(20), timestamp varchar(20)")
exec_sql(db_conn, "copy darpa_sample(source, destination, timestamp) from '%s' delimiter ','" % path)
print "Data copied to table darpa_sample"
close_db(db_conn)
exit(0)
