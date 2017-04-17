import sys
import os
from DCube_sql import *

data_path = "D:/dataset/datasets/darpa_with_label.csv"
exp_conn = connect_db()

try:
    for density in ("ari", "geo", "sus"):
        for dimension in ("dense", "card"):
            os.system("python import_datafile_to_database.py %s" % data_path)
            os.system("python DCube_main.py %s %s" % (density, dimension))
            drop_table(exp_conn, "darpa_parameters_%s_%s" % (density, dimension))
            exec_sql(exp_conn, "alter table darpa_sample_parameters rename to darpa_parameters_%s_%s" % (density, dimension))
            drop_table(exp_conn, "darpa_results_%s_%s" % (density, dimension))
            exec_sql(exp_conn, "alter table darpa_sample_results rename to darpa_results_%s_%s" % (density, dimension))
except KeyboardInterrupt:
    print "exit manually"
    raise
finally:
    close_db(exp_conn)
    exit(0)