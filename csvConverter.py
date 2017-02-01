import sys, os

# designed to convert .txt w/spaces to .csv file
def parseFile(infile=None):
    outfile=""

    # creates output directory for files if directory does not exist
    if not os.path.exists("output"):
        os.makedirs("output")

    # Converts the .txt filename into .csv filename
    if ".csv" not in infile:
        outfile=infile[0:len(infile)-4] + ".csv"
        print outfile
    else:
        print "Please provide a file to be converted to csv"
        exit()

    try:
        read_file = open(infile,"r+")
        write_file = open("output/"+outfile,"w")
    except:
        print "Cannot open given file " + str(infile) + " or " + str(outfile)

    for line in read_file:
        new_line = line.split()
        out_string = form_output_string(new_line)
        write_file.write(out_string+'\n')

    # cleanup of open files
    read_file.close()
    write_file.close()


def form_output_string(elementlist):
    output_string = ""
    for element in elementlist:
        if elementlist.index(element) < len(elementlist):
            output_string += element + ','
    output_string = output_string[:-1]
    return output_string

def main():
    if len(sys.argv) > 1:
        input = str(sys.argv[1])
    else:
        print "Usage: python tabReplace.py [filename]"
        exit()
    parseFile(infile=input)


if __name__ == "__main__":
    main()
