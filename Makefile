# run D-Cube on darpa.csv

# change path to darpa.csv here
# data_path = /Users/lipeilun/Documents/dataset/datasets/darpa.csv
# resultfolder_path = /Users/lipeilun/Documents/dataset/datasets/darpa.csv
data_path = /Users/zhouchangkai/Desktop/CMU/course/15826/Project/datasets/darpa_with_label.csv
resultfolder_path = /Users/zhouchangkai/Desktop/CMU/course/15826/Project/darpa_output_2

all:
	@python import_darpa_to_database.py $(data_path)
	@echo "Start running D-Cube"
	@echo "You can change density measure, density selection and other parameters in DCube_params.py"
	@python DCube_main.py

roc:
	@python import_darpa_to_database.py $(data_path)
	@python import_resultfile_to_database.py $(resultfolder_path)
	@echo "Start evaluate results of D-Cube and draw ROC curve with the value of AUC."
	@python DCube_evaluation.py
