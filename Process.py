#!/usr/bin/env python3
import glob, os
import xml.etree.ElementTree as ET

PATH='/home/quantics/public_html/static/'
os.chdir(PATH)

for file in glob.glob(PATH+"*0.xml"):
    tree = ET.parse(file)
    root = tree.getroot()
    for GasStation in root:
        print(GasStation.attrib[2])



for file in glob.glob("*1.xml"):
    tree = ET.parse(file)
    root = tree.getroot()
