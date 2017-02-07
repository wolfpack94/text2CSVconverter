import sys, os

def pull_row_len(line):
    split_line = line.split(',')
    return len(split_line)


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

    cols = pull_row_len(input_file.readline())
    num_occurrences = 0
    if cols > 0:
        for line in input_file:
            split_line = line.split(',')
            if not validate_row(split_line,cols):
                num_occurrences += 1
                output_file.write("Line found: \n"+line+"\n")
        output_file.write("Number of records with differences: "+str(num_occurrences))


def main():
    input_file = None

    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    parse_file(input_file)

    print "Analysis Complete"

if __name__ == "__main__":
    main()
