#!/usr/bin/env python3
import glob, os
import xml.etree.ElementTree as ET

PATH='/home/quantics/public_html/static/'
os.chdir(PATH)

for file in glob.glob(PATH+"*0.xml"):
    tree = ET.parse(file)
    root = tree.getroot()
    for GasStation in root:
        id = GasStation.get('place_id')
        name = GasStation.find('name').text
        location = GasStation.find('location')
        print(id,name,location.x)


for file in glob.glob("*1.xml"):
    tree = ET.parse(file)
    root = tree.getroot()
