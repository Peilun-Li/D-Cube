# run D-Cube on darpa.csv

# change path to darpa.csv here
data_path = /Users/lipeilun/Documents/dataset/datasets/darpa.csv
resultfolder_path = /Users/lipeilun/Documents/dataset/datasets/darpa.csv
# data_path_darpa = /Users/zhouchangkai/Desktop/CMU/course/15826/Project/datasets/darpa_with_label.csv
# data_path_airforce = /Users/zhouchangkai/Desktop/CMU/course/15826/Project/datasets/airforce_with_label.csv
# resultfolder_path_darpa = /Users/zhouchangkai/Desktop/CMU/course/15826/Project/darpa_output
# resultfolder_path_airforce = /Users/zhouchangkai/Desktop/CMU/course/15826/Project/airforce_output

all:
	@python import_darpa_to_database.py $(data_path)
	@echo "Start running D-Cube"
	@echo "You can change density measure, density selection and other parameters in DCube_params.py"
	@python DCube_main.py

roc:
	# @python import_darpa_to_database.py $(data_path_darpa)
	@python import_airforce_to_database.py $(data_path_airforce)
	# @python import_darpa_resultfile_to_database.py $(resultfolder_path_darpa)
	@python import_airforce_resultfile_to_database.py $(resultfolder_path_airforce)
	# @echo "Start evaluate results of D-Cube and draw ROC curve with the value of AUC."
	@python DCube_evaluation.py
