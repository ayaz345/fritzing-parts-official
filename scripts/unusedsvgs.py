
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
    unusedsvgs.py -f [fzp folder] -s [svg folder]
    lists orphan svgs
""")


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:s:", [
                                   "help", "fzp", "svg"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)
        usage()
        return

    fzpdir = None
    svgdir = None

    for o, a in opts:
        # print o
        # print a
        if o in ("-f", "--fzp"):
            fzpdir = a
        elif o in ("-s", "--svg"):
            svgdir = a
        elif o in ("-h", "--help"):
            usage()
            return
        else:
            print("unhandled option", o)
            return

    if not fzpdir:
        print("missing fzp folder argument")
        usage()
        return

    if not svgdir:
        print("missing svg folder argument")
        usage()
        return

    svgfiles = {}
    for root, dirs, files in os.walk(svgdir, topdown=False):
        for filename in files:
            if not filename.endswith(".svg"):
                continue

            basename = os.path.basename(root)
            if svgfiles.get(basename) is None:
                svgfiles[basename] = []

            svgfiles[basename].append(filename)

    viewnames = ["iconView", "breadboardView", "schematicView", "pcbView"]

    for root, dirs, files in os.walk(fzpdir, topdown=False):
        for filename in files:
            if not filename.endswith(".fzp"):
                continue

            fzpFilename = os.path.join(root, filename)
            try:
                dom = xml.dom.minidom.parse(fzpFilename)
            except xml.parsers.expat.ExpatError as err:
                print(err, fzpFilename)
                continue

            fzp = dom.documentElement
            for viewname in viewnames:
                viewNodes = fzp.getElementsByTagName(viewname)
                for viewNode in viewNodes:
                    layersNodes = viewNode.getElementsByTagName("layers")
                    for layersNode in layersNodes:
                        image = layersNode.getAttribute("image")
                        dn = os.path.dirname(image)
                        if viewFiles := svgfiles.get(dn):
                            fn = os.path.basename(image)
                            try:
                                if fn in viewFiles:
                                    print(
                                        "{0} uses {1}/{2}".format(os.path.basename(root), dn, fn))
                                    viewFiles.remove(fn)
                            except:
                                pass

    count_unsued = 0
    for key in svgfiles:
        for name in svgfiles.get(key):
            print("unused {0}/{1}".format(key, name))
            count_unsued += 1

    print("Unused svg files found: %d" % count_unsued)
    return -1 if count_unused>2318 else 0

if __name__ == "__main__":
    sys.exit(main())
