PYTHON=python3
PROG=dataValidation.py
W_FOLDER=../Datasets/StormEvents/Details/
W_FILE=storm_details_2014.csv
B_FOLDER=../Datasets/CDC/
B_FILE=natality2014.txt
C_FILE=../Datasets/countyEstimate2014.csv

test:
	$(PYTHON) $(PROG) $(B_FOLDER)$(B_FILE) $(W_FOLDER)$(W_FILE) $(C_FILE)
