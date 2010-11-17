#!c:/Python/python.exe -u
# $ checkimages.py /path/to/files

import EXIF
import glob
import sys
import Image
from shutil import copy2

filenum = 0
bitdepthnum = 0
lzw = 0
for file in glob.iglob(sys.argv[1]):
    filenum += 1
    try: 
        tags = EXIF.process_file(open(file))
        res = tags['Image YResolution'].printable
        compr = tags['Image Compression'].printable
        date = tags['Image DateTime'].printable

        if res != '300':
            print "File: %s  Res: %s dpi  Date: %s" % (file, res, date)    

        if compr != 'LZW':
            copy2(file, 'u:/image_sandbox/compress')
            lzw += 1

    except:
        print "Can't read EXIF tags: %s" % (file)

    try:
        i = Image.open(file)
    except IOError:
        copy2(file, 'u:/image_sandbox/bitdepthissues/')
        bitdepthnum += 1

    
itemnum = file[14:17]
print 
print "------------------"
print "%d total files" % (filenum)
print "%s total items" % (itemnum)
if bitdepthnum:
    print "%d total bitdepth issues" % (bitdepthnum)
if lzw:
    print "%d total uncompressed images" % (lzw)
