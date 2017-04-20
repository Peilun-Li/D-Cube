DEBUG = True

PSQL_DB = "postgres"
PSQL_DB_USER = "user"
PSQL_DB_PWD = "password"
PSQL_DB_PORT = 5432

dataset = "darpa"

if dataset == "darpa":
    # relation/table name
    relation = "darpa_sample"
    # k is number of dense blocks to find
    k = 20
    # column names for dimension attributes
    dimension_attributes = ["source", "destination", "timestamp"]
    # column name for measure attribute, or empty "" if the mass is just count of rows
    measure_attribute = ""
    # density measure can be ari, geo or sus,
    # where ari = arithmetic arithmetic average degree, geo = geometric average degree, sus = suspiciousness
    density_measure = "ari"
    # dimension selection can be dense or card,
    # where dense = maximum density first, card = maximum cardinality first
    dimension_selection = "dense"
    # max length of strings in dimension_attributes
    max_len_of_attributes = 20
elif dataset == "airforce":
    relation = "airforce_sample"
    k = 20
    dimension_attributes = ["protocol", "service", "flag", "src_bytes", "dst_bytes", "host_cnt", "srv_cnt"]
    measure_attribute = ""
    density_measure = "ari"
    dimension_selection = "dense"
    max_len_of_attributes = 20
elif dataset == "syn":
    relation = "syn"
    k = 2
    dimension_attributes = ["field1", "field2", "field3"]
    measure_attribute = ""
    density_measure = "ari"  # ari, geo, sus
    dimension_selection = "dense"  # dense, card
    max_len_of_attributes = 9
elif dataset == "syn2":
    relation = "syn2"
    k = 1
    dimension_attributes = ["a0", "a1", "a2", "a3"]
    measure_attribute = ""
    density_measure = "ari"  # ari, geo, sus
    dimension_selection = "dense"  # dense, card
    max_len_of_attributes = 9
elif dataset == "videos":
    relation = "videos_sample"
    k = 1
    dimension_attributes = ["username", "item", "timestamp", "rating"]
    measure_attribute = ""
    density_measure = "sus"
    dimension_selection = "dense"
    max_len_of_attributes = 9