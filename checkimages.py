#!c:/Python/python.exe -u
# $ checkimages.py resolution /path/to/files

import EXIF
import glob
import sys
import Image
import TiffImagePlugin
from shutil import copy2

dpi = sys.argv[1]

filenum = 0
bitdepthnum = 0
lzw = 0

for filename in glob.iglob(sys.argv[2]):
    filenum += 1
    try: 
        tags = EXIF.process_file(open(filename))
        res = tags['Image YResolution'].printable
        compr = tags['Image Compression'].printable
        date = tags['Image DateTime'].printable

        if res != dpi:
            print "File: %s  Res: %s dpi  Date: %s" % (filename, res, date)    

        if compr != 'LZW':
            copy2(filename, 'c:/image_sandbox/compress')
            lzw += 1

    except:
        print "Can't read EXIF tags: %s" % (filename)

    try:
        i = Image.open(filename)
    except IOError:
        copy2(filename, 'c:/image_sandbox/bitdepthissues/')
        bitdepthnum += 1

    
print 
print "------------------"
print "%d total files" % (filenum)
if bitdepthnum:
    print "%d total bitdepth issues" % (bitdepthnum)
if lzw:
    print "%d total uncompressed images" % (lzw)
