from DCube_params import *
from DCube_sql import *
import sys
import os

path = os.path.abspath("syn.csv")

if not os.path.exists(path):
    print "Error: could not find data file. Please modify the data_path parameter in Makefile to the path of syn.csv"
    exit(-1)
path = os.path.abspath(path)

try:
    db_conn = connect_db()
except:
    print "Error: could not connect to database. Please modify psql account/port information in DCube_params.py to connect to psql"
    exit(-1)

try:
    print "Copying data..."
    drop_and_create_table(db_conn, "syn", "field1 integer, field2 integer, field3 integer")
    exec_sql(db_conn, "copy syn(field1, field2, field3) from '%s' delimiter ','" % path)
    print "Data copied to table syn"
except KeyboardInterrupt:
    print "exit manually"

close_db(db_conn)
exit(0)
