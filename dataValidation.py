import sys, os

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

    print output_file

    if os.path.isfile(output_file):
        prompt=str(raw_input("File "+output_file+" found, would you like to overwrite file? "))
        if prompt == 'y':
            overwrite = True
            FLAG = 'w'

    try:
        input_file = open(infile,'r')
        output_file = open(output_file,FLAG)
    except:
        print "File " + input_file + " cannot be opened."
        exit()

    cols = pull_max_row_len(input_file)
    print cols
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


def main():
    input_file = None

    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        print "Usage: python dataValidation.py [input file]"
        exit()

    occurrences = parse_file(input_file)

    print "Analysis Complete"
    print "Records found: " + str(occurrences)

if __name__ == "__main__":
    main()
