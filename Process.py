#!/usr/bin/env python3
import glob, os

PATH='/home/quantics/public_html/static/'
os.chdir("/home/quantics/public_html/static/backup/")

for file in glob.glob("*0.xml"):
    print(file,"locs")

for file in glob.glob("*1.xml"):
    print(file,"prices")
