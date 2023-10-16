
import getopt
import sys
import os
import os.path
import re
import xml.dom.minidom
import xml.dom


def usage():
    print("""
usage:
    listModuleIDs.py -f { fz file }
    looks for files where copper0/copper1 are not parent/child or child/parent

    Warning: This script is incomplete, no reference to copper0 or copper1 is done below.
""")


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:", ["help", "file"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)
        usage()
        return

    filename = None

    for o, a in opts:
        # print o
        # print a
        if o in ("-f", "--file"):
            filename = a
        elif o in ("-h", "--help"):
            usage()
            return
        else:
            assert False, "unhandled option"

    if filename is None:
        usage()
        return

    try:
        dom = xml.dom.minidom.parse(filename)
    except xml.parsers.expat.ExpatError as err:
        print(err, filename)
        return

    moduleIDs = {}

    root = dom.documentElement
    instances = root.getElementsByTagName("instance")
    for instance in instances:
        moduleID = instance.getAttribute("moduleIdRef")
        path = instance.getAttribute("path")
        if moduleIDs.get(moduleID) is None:
            moduleIDs[moduleID] = path

    for moduleID in moduleIDs:
        print(moduleID)
        print("    ", moduleIDs[moduleID])


if __name__ == "__main__":
    main()
