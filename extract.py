#!c:/Python/python.exe -u

# Recursively check for and extract files from a list of item ids.  
# Optionally transform MODS to DC and convert TIFFs to 100dpi JPEGs
#
# extract.py -h for list of options
#
# For simple extract of TIFFs and metadata:
# $ extract.py -l /path/to/itemlist -o /path/to/outdirectory/ .
#
# To convert to JPEGs and include DC metadata:
# $ extract.py -j -d -l /path/to/itemlist -o /path/to/outdirectory/ .


import os, sys
import Image
from shutil import copy2
from lxml import etree
from optparse import OptionParser

usage = "usage: %prog [options] startdir"
parser = OptionParser(usage=usage)

parser.add_option("-l", dest="list", help="List of items to extract")
parser.add_option("-o", dest="outdir", help="Specify output directory")
parser.add_option("-j", action="store_true", dest="jpeg", help="Convert tiff to jpeg")
parser.add_option("-m", action="store_true", dest="metadata", help="Include metadata with files")
parser.add_option("-d", action="store_true", dest="dc", help="Create DC record.  Used with -m option")

(options, args) = parser.parse_args()

f = open(options.list)
dest = options.outdir

names = [line.strip() for line in f.readlines()] 

for path, dirs, files in os.walk(args[0]):
    for filename in files:
        name, ext = os.path.splitext(filename)
        if name[:17] in names:
            file = os.path.join(path, filename)
            if ext == ".tif":
                if options.jpeg:
                    im = Image.open(file)
                    im.save(dest + name + '.jpg')
                else:
                    copy2(file, dest)
            if ext == ".xml" and options.metadata:
                tree = etree.parse(file)
                if name[18:] == 'tei':
                    tree.write(dest + file)
                elif options.metadata and options.dc:
                    tree = etree.parse(file)
                    tree.write(dest + name + '-mods.xml')
                    xslt_doc = etree.parse('u:/MODS3-22simpleDCmodAR.xsl')
                    transform = etree.XSLT(xslt_doc)
                    result = transform(tree)
                    result.write(dest + name + '-dc.xml')
                else:
                    copy2(file, dest)



        






            
