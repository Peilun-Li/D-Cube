import sys
import os
from DCube_sql import *

data_path = "D:/dataset/datasets/airforce_with_label.csv"
exp_conn = connect_db()
dimension_attributes = "['protocol','service','flag','src_bytes','dst_bytes','host_cnt','srv_cnt']"
relation = "airforce_sample"

try:
    for density in ("ari", "geo", "sus"):
        for dimension in ("dense", "card"):
            os.system("python import_airforce_to_database.py %s" % data_path)
            os.system("python DCube_main.py %s %s %s %s" % (density, dimension, relation, dimension_attributes))
            drop_table(exp_conn, "airforce_parameters_%s_%s" % (density, dimension))
            exec_sql(exp_conn, "alter table airforce_sample_parameters rename to airforce_parameters_%s_%s" % (density, dimension))
            drop_table(exp_conn, "airforce_results_%s_%s" % (density, dimension))
            exec_sql(exp_conn, "alter table airforce_sample_results rename to airforce_results_%s_%s" % (density, dimension))
except KeyboardInterrupt:
    print "exit manually"
    raise
finally:
    close_db(exp_conn)
    exit(0)