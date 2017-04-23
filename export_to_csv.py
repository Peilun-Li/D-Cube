
with open("darpa_export_script.txt", "w") as f:
	for density in ("ari", "geo", "sus"):
		for dimension in ("dense", "card"):
			f.write( "\copy (select * from darpa_parameters_%s_%s) to 'D:\\dataset\\darpa_output\\darpa_parameters_%s_%s.csv' delimiter ',' csv header \n\n" % (density, dimension, density, dimension))
			f.write( "\copy (select * from darpa_results_%s_%s) to 'D:\\dataset\\darpa_output\\darpa_results_%s_%s.csv' delimiter ',' csv header \n\n" % (density, dimension, density, dimension))

			
			