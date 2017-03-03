PYTHON=python3
PROG=dataValidation.py
W_FOLDER=../Datasets/StormEvents/Details/
W_FILE=storm_details_2015.csv
B_FOLDER=../Datasets/CDC/
B_FILE=natality2015.txt

test:
	$(PYTHON) $(PROG) $(B_FOLDER)$(B_FILE) $(W_FOLDER)$(W_FILE) 
