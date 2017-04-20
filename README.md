# D-Cube
CMU 15-826 Project (17 Spring)


Usage:
1. modify the data_path parameter in Makefile to the path of darpa.csv (without label)
2. modify postgresql account, database and port information in DCube_params.py to connect to postgresql
3. (if host is not localhost, please change the connect code in connect_db() function of DCubte_sql.py)
4. run Makefile, which will run D-Cube using darpa.csv
5. the results of D-Cube will be saved in table darpa_sample_results and darpa_sample_parameters

