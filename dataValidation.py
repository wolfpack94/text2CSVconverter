import sys, os
import pandas as pd

def pull_max_row_len(infile):
    max_len = 0
    for line in infile:
        split_line = line.split(',')
        if len(split_line) > max_len:
            max_len = len(split_line)
    return max_len


def validate_row(line,columns):
    if len(line) == columns:
        return True
    else:
        return False


def parse_file(infile=None):
    output_file = "analysis"
    overwrite = False
    FLAG = 'a'

    output_file = output_file + infile[infile.index('2'):infile.index('.')] + ".dat"

    print(output_file)

    if os.path.isfile(output_file):
        prompt=str(eval(input("File "+output_file+" found, would you like to overwrite file? ")))
        if prompt == 'y':
            overwrite = True
            FLAG = 'w'

    try:
        input_file = open(infile,'r')
        output_file = open(output_file,FLAG)
    except:
        print(("File " + input_file + " cannot be opened."))
        exit()

    cols = pull_max_row_len(input_file)
    print(cols)
    input_file.seek(0)
    num_occurrences = 0
    if cols > 0:
        for line in input_file:
            split_line = line.split(',')
            if not validate_row(split_line,cols):
                num_occurrences += 1
                output_file.write("Line found: \n"+"Length of line: "+str(len(split_line))+" Supposed length: "+str(cols)+"\n"+line+"\n")
        output_file.write("Number of records with differences: "+str(num_occurrences))
    return num_occurrences


'''
Removes rows with nan
'''
def clean(df):
    length = len(df)
    df = df.dropna()
    print((str(length - len(df)) + "/" + str(length) + " Rows cleaned"))
    return df


def import_data(filename, delim):
    try:
        data = pd.read_csv(filename, sep=delim)
    except:
        print("Failed to open " + filename);
    return data 


def pad_values_2(x):
    return str(x).zfill(2)


def pad_values_3(x):
    return str(x).zfill(3)


def main():
    b_file = None
    w_file = None

    if len(sys.argv) > 1:
        b_file = sys.argv[1]
        w_file = sys.argv[2]

    else:
        print("Usage: python dataValidation.py [input file]")
        exit()

    b_df = import_data(b_file,"\t")
    w_df = import_data(w_file,",")

    #Convert to dataframe
    print("Selecting relevant dimensions for " + b_file)
    b_df = pd.DataFrame(b_df, columns=["State Code", "County Code", "Year", "Month Code", "Births"])
    print("Selecting relevant dimensions for " + w_file)
    w_df = pd.DataFrame(w_df, columns=["STATE_FIPS", "CZ_FIPS", "BEGIN_YEARMONTH", "EVENT_TYPE"])

    #Data cleaning
    print("Cleaning file " + b_file)
    b_df = clean(b_df)
    print("Cleaning file " + w_file)
    w_df = clean(w_df)

    #Integration
    w_df['FIPS'] = w_df["STATE_FIPS"].apply(pad_values_2) + w_df["CZ_FIPS"].apply(pad_values_3)
    grouped = w_df.groupby(['FIPS', 'BEGIN_YEARMONTH', 'EVENT_TYPE']).size()
    #print(w_df.columns)
    #print(grouped)

    b_df['YEAR_MONTH'] = b_df["Year"].map(str) + b_df["Month Code"].apply(pad_values_2)
    print(b_df.values[-30:-1])

    print("Analysis Complete")

if __name__ == "__main__":
    main()
