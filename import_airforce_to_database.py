from DCube_params import *
from DCube_sql import *
import sys
import os

path = sys.argv[1]
bucketize = False

if "label" in path:
    with_label = True
else:
    with_label = False

if not os.path.exists(path):
    print "Error: could not find data file. Please modify the data_path parameter in Makefile to the path of darpa.csv (without label)"
    exit(-1)
path = os.path.abspath(path)

try:
    db_conn = connect_db()
except:
    print "Error: could not connect to database. Please modify psql account/port information in DCube_params.py to connect to psql"
    exit(-1)

try:
    print "Copying data..."
    if with_label:
        drop_and_create_table(db_conn, "airforce_sample", "protocol varchar, service varchar, flag varchar, src_bytes integer, dst_bytes integer, host_cnt integer, srv_cnt integer, label varchar")
        exec_sql(db_conn, "copy airforce_sample(protocol, service, flag, src_bytes, dst_bytes, host_cnt, srv_cnt, label) from '%s' delimiter ','" % path)
    else:
        drop_and_create_table(db_conn, "airforce_sample", "protocol varchar, service varchar, flag varchar, src_bytes integer, dst_bytes integer, host_cnt integer, srv_cnt integer")
        exec_sql(db_conn, "copy airforce_sample(protocol, service, flag, src_bytes, dst_bytes, host_cnt, srv_cnt) from '%s' delimiter ','" % path)
    
    #if bucketize:
    #    exec_sql(db_conn, "alter table darpa_sample alter column timestamp type varchar(13) using SUBSTR(timestamp, 1, 13)")
    #    drop_and_copy_table(db_conn, "darpa_sample", "darpa_sample_distinct", "distinct on (source, destination, timestamp) *")
    #    drop_table(db_conn, "darpa_sample")
    #    exec_sql(db_conn, "alter table darpa_sample_distinct rename to darpa_sample")
    print "Data copied to table airforce_sample"
except KeyboardInterrupt:
    print "exit manually"

close_db(db_conn)
exit(0)
