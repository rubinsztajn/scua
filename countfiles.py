#!c:/Python/python.exe -u

import os, sys, time
import win32security
from optparse import OptionParser

usage = "usage: %prog [options] startdir"
parser = OptionParser(usage=usage)

parser.add_option("-p", dest="pattern", help="Pattern to match against filenames")
parser.add_option("-r", dest="drange", help="Specify date range: YYYYMMDD-YYYYMMDD")
parser.add_option("-n", action="store_true", dest="names")

(options, args) = parser.parse_args()

    
i = 0  # Iterator for total count
t = 0  # Iterator for date range count
names = {} # List of file owners

for path, dirs, files in os.walk(args[0]):
    for filename in files:
        if filename.find(options.pattern) != -1:
            i += 1
            if options.drange:
                start, end = options.drange.split('-') 
                filepath = os.path.join(path, filename)
                stats = os.stat(filepath)
                date = time.strftime("%Y%m%d", time.localtime(stats.st_ctime))
                if (int(date) >= int(start)) and (int(date) <= int(end)):
                    t += 1
                    if options.names:
                        sd = win32security.GetFileSecurity(filepath, win32security.OWNER_SECURITY_INFORMATION)
                        owner_sid = sd.GetSecurityDescriptorOwner()
                        owner_name, domain, type = win32security.LookupAccountSid(None, owner_sid)
                        if owner_name in names:
                            names[owner_name] += 1
                        else:
                            names[owner_name] = 1
            

print "-" * 10
if options.drange:
    print "Total files created between %s and %s: %d" % (start, end, t)  
if options.names:
    for x in names:
        print "%s: %d" % (x, names[x])

print "Total files:", i
