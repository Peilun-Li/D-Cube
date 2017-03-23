# run D-Cube on darpa.csv

# change path to darpa.csv here
data_path = /Users/lipeilun/Documents/dataset/datasets/darpa.csv

all:
	@python import_datafile_to_database.py $(data_path)
	@echo "Start running D-Cube"
	@echo "You can change density measure, density selection and other parameters in DCube_params.py"
	@python DCube_main.py