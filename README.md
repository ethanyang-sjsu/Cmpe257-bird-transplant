# Setup
Your directory structure should look like:
```
data/	# Training data obtained from GetTrainData.ipynb. The files can be found at:
		# https://drive.google.com/drive/u/2/folders/0AKCoaEnqOZeuUk9PVA
sb/
ebird_api.key	# This is excluded from the repo via git ignore. This is only
				# needed if you want to make API queries (such as via
				# GetTrainData.ipynb). You do NOT need to make API queries if
				# you've already loaded the data into the data/ directory.
				#
				# If you really want, you can request API access at:
				# https://ebird.org/data/download
ebirdtools.py
GetTrainData.ipynb	# Optional. Only usable if ebird_api.key is valid.
```

# Credits
Ethan:
- GetTrainData.ipynb
- NaiveClusterDemo.ipynb
- ebirdtools.py
- sb/sb01-sb05
- sb/sb06_kmeanstest.ipynb
- sb/sb07_dbscantest.ipynb

Inderpreet:
- sb/sb08_knn_temp_distance_anomalies_hotspots.ipynb

Andy:
- sb/sb09_generate_elevation.ipynb
