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
        cre_id = GasStation.find('cre_id').text
        location = GasStation.find('location')
        x = location.find('x').text
        y = location.find('y').text
        #print(id,(x,y))


for file in glob.glob("*1.xml"):
    tree = ET.parse(file)
    root = tree.getroot()
    for place in root:
        id = place.get('place_id')
        for gas_price in place.iter('gas_price'):

            print(gas_price.attrib['type'])
