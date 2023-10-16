# usage:
#    droid.py -d <directory>
#
#    <directory> is a folder, with subfolders, containing .svg files.  In each svg file in the directory or its children
#    replace 'Droid Sans' with DroidSans

import getopt
import sys
import os
import re


def usage():
    print("""
usage:
    droid.py -d [directory]
    
    directory is a folder containing .svg files.  
    In each svg file in the directory or its subfolders,
    replace 'Droid Sans' with DroidSans.
    """)


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:", ["help", "directory"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)
        usage()
        sys.exit(2)
    outputDir = None

    for o, a in opts:
        # print o
        # print a
        if o in ("-d", "--directory"):
            outputDir = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit(2)
        else:
            assert False, "unhandled option"

    if(not(outputDir)):
        usage()
        sys.exit(2)

    for root, dirs, files in os.walk(outputDir, topdown=False):
        for filename in files:
            if (filename.endswith(".svg")):
                with open(os.path.join(root, filename), "r") as infile:
                    svg = infile.read()
                svg1 = svg.replace("'Droid Sans'", "DroidSans")
                svg2 = svg1.replace("Droid Sans", "DroidSans")
                svg3 = svg2.replace("'DroidSans'", "DroidSans")

                if (len(svg3) != len(svg)):
                    with open(os.path.join(root, filename), "w") as outfile:
                        outfile.write(svg3)
                    print("{0}".format(os.path.join(root, filename)))


if __name__ == "__main__":
    main()
