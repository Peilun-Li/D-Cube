# Dense Subtensor Mining using SQL
This is a implementation of [D-Cube](http://www.cs.cmu.edu/~kijungs/papers/dcubeWSDM2017.pdf) using SQL. (also a CMU 15-826 17 spring course project)

Dependencies:
1. PostgreSQL
2. psycopg2

General Usage:
1. Configure postgresql connection parameters in `DCube_params.py`, i.e., postgresql account, database and port information. If the host is not localhost, please change the connect code in connect_db() function of DCubte_sql.py.
2. Import your data to the database. For example, import airforce.csv as a relation `darpa`, with the dimension attributes `source`, `destination` and `timestamp`.
3. You can either:
   1. Modify density measure, density selection and other parameters in DCube_params.py. And then run `python DCube_main.sql`, or
   2. Run `python DCube_main.sql density_measure dimension_selection relation dimension_attributes k`, where density_measure can be ari, geo or sus, dimension_selection can be dense or card, dimension_attributes is the list of dimension attributes, and k is the number of dense blocks to retrieve. Example: `python DCube_main.sql ari dense darpa "['source','destination`','timestamp`']" 2` (pay attention to the format of dimension_attributes)
4. The results of D-Cube will be saved in table $(relation)_results and $(relation)_parameters. For example, darpa_results (for the content of dense blocks) and darpa_parameters (time, count and density of dense blocks)


Specific Usage for Experiments/Submmissions:
1. The make command will run D_Cube on a small synthetic dataset, which is generated by `generate_synthetic_data.py`
1. If you want to run experiments on darpa or airforce, modify the `data_path` parameter in `darpa_experiments.py` or `airforce_experiments.py`, then run them as python scripts.

