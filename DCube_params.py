DEBUG = True

PSQL_DB = "postgres"
PSQL_DB_USER = "postgres"
PSQL_DB_PWD = "password"
PSQL_DB_PORT = 5432

"""
relation = "videos_sample"
k = 5
# dimension_attributes = ["username", "item", "timestamp"]
# measure_attribute = "rating" # or "" if just count tuples
dimension_attributes = ["username", "item", "timestamp", "rating"]
measure_attribute = ""
density_measure = "sus"  # ari, geo, sus
dimension_selection = "dense"  # dense, card
max_len_of_attributes = 9
"""

relation = "syn"
k = 2
dimension_attributes = ["field1", "field2", "field3"]
measure_attribute = ""
density_measure = "ari"  # ari, geo, sus
dimension_selection = "card"  # dense, card
max_len_of_attributes = 9