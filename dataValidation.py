import sys, os
import pandas as pd
import numpy as np

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
    df = df.round()
    print((str(length - len(df)) + "/" + str(length) + " Rows cleaned"))
    return df


def import_data(filename, delim):
    try:
        data = pd.read_csv(filename, sep=delim, encoding="ISO-8859-1")
    except:
        print("Failed to open " + filename);
        exit()
    return data


def pad_values_2(x):
    return str(x).zfill(2)


def pad_values_3(x):
    return str(x).zfill(3)[-3:]


def categorize_weather(weather_type, output_file=None):
    level_interp = {"l":"low", "m":"moderate", "h":"high"}
    for weather in weather_type:
        level = str(input("Enter level for {} [l:low, m:moderate, h:high]: ".format(weather)))
        expanded = level_interp[level]
        output_file.write("{},{}\n".format(weather, expanded))
    if output_file:
        output_file.close()


def main():
    mapped_events = {}
    LEVELS = "../Datasets/levels.txt"
    levels_file = None
    levels_read = None
    b_file = None
    w_file = None
    c_file = None
    unique_w_event = ['YEAR_MONTH', 'FIPS', 'TOTAL_BIRTHS']

    if len(sys.argv) > 1:
        b_file = sys.argv[1]
        w_file = sys.argv[2]
        c_file = sys.argv[3]

    else:
        print("Usage: python dataValidation.py [input file]")
        exit()

    if not os.path.isfile(LEVELS):
        try:
            levels_file = open(LEVELS, "w")
        except:
            print("Failed to open")
            exit()
    else:
        try:
            levels_read = open(LEVELS, "r")
            # read levels file into dictionary for assimilation
            for line in levels_read:
                line = line.strip('\n')
                split = line.split(",")
                mapped_events[split[0]] = split[1]
        except:
            print("Failed to open {} for reading level data.".format(LEVELS))
            print("Exiting...")
            exit()

    b_df = import_data(b_file,"\t")
    w_df = import_data(w_file,",")
    c_df = import_data(c_file,",")

    #Convert to dataframe
    print("Selecting relevant dimensions for " + b_file)
    b_df = pd.DataFrame(b_df, columns=["State Code", "County Code", "Year", "Month Code", "Births"])
    print("Selecting relevant dimensions for " + w_file)
    w_df = pd.DataFrame(w_df, columns=["STATE_FIPS", "CZ_FIPS", "BEGIN_YEARMONTH", "EVENT_TYPE"])
    print("Selecting relevant dimensions for " + c_file)
    c_df = pd.DataFrame(c_df, columns=["STATE", "COUNTY", "POPESTIMATE2014"])

    #Data cleaning
    print("Cleaning file " + b_file)
    b_df = clean(b_df)
    print("Cleaning file " + w_file)
    w_df = clean(w_df)
    print("Cleaning file " + c_file)
    c_df = clean(c_df)

    #Cleaning set of state population data
    c_df = c_df[c_df.COUNTY != 0]

    #Type casting values to int
    b_df = b_df.astype(int)

    #Integration
    w_df['FIPS'] = w_df["STATE_FIPS"].apply(pad_values_2) + w_df["CZ_FIPS"].apply(pad_values_3)
    b_df['FIPS'] = b_df["State Code"].apply(pad_values_2) + b_df["County Code"].apply(pad_values_3)
    b_df['YEAR_MONTH'] = b_df["Year"].map(str) + b_df["Month Code"].apply(pad_values_2)
    w_df.rename(columns={'BEGIN_YEARMONTH':'YEAR_MONTH'}, inplace=True)
    c_df['FIPS'] = c_df["STATE"].apply(pad_values_2) + c_df["COUNTY"].apply(pad_values_3)
    c_df.to_csv('merged_census.csv', ',')
    grouped = w_df.groupby(['YEAR_MONTH', 'FIPS'], as_index=False)['EVENT_TYPE'].count()

    combined = pd.DataFrame(columns=['YEAR_MONTH', 'FIPS', 'TOTAL_BIRTHS', 'TOTAL_HIGHLOW', 'PERCAPITA'])

    b_df = b_df[(b_df.FIPS.str.len() == 5)]

    # pulls unique weather events and puts them into a list
    unique = w_df['EVENT_TYPE'].unique()
    if levels_file:
        categorize_weather(unique, levels_file)
    
    for name in grouped.values:
        yearmonth = str(name[0])
        fips = str(name[1])
        pull_births = b_df[(b_df.YEAR_MONTH == yearmonth) & (b_df.FIPS == fips)]
        pull_pop = c_df[(c_df.FIPS == fips)]
        if not pull_births.empty and not pull_pop.empty:
            percapita = float(pull_births.Births.values[0]) / float(pull_pop.POPESTIMATE2014.values[0])
            df = pd.DataFrame(data=[(name[0], name[1], pull_births.Births.values[0], name[2], percapita)], columns=['YEAR_MONTH', 'FIPS', 'TOTAL_BIRTHS', 'TOTAL_HIGHLOW', 'PERCAPITA']) 
            combined = combined.append(df, ignore_index=True)

    combined.to_csv('../Datasets/Integrated2014.csv', ',', encoding="ISO-8859-1")

    print("Analysis Complete")

if __name__ == "__main__":
    main()
