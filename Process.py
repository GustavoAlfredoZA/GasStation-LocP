#!/usr/bin/env python3
import glob, os
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json

p = open("routes.json")
routes = json.load(p)
ProyectPATH=routes['proyect']
PublicPATH=routes['public']
p.close()

with open('db.json') as json_file:
    config = json.load(json_file)

os.chdir(PublicPATH)
X=[]
Y=[]

for file in glob.glob(PublicPATH+"*0.xml"):
    tree = ET.parse(file)
    root = tree.getroot()
    for GasStation in root:
        id = GasStation.get('place_id')
        name = GasStation.find('name').text
        cre_id = GasStation.find('cre_id').text
        location = GasStation.find('location')
        x = location.find('x').text
        y = location.find('y').text
        X.append(x)
        Y.append(y)

for file in glob.glob(PublicPATH+"*1.xml"):
    tree = ET.parse(file)
    root = tree.getroot()
    for place in root:
        id = place.get('place_id')
        for gas_price in place.iter('gas_price'):
            type=gas_price.attrib['type']
            price=gas_price.text
            #print(gas_price.attrib['type'],price)

fig = plt.figure()
#ax = plt.subplots()
#ax.set(title='Gas Station Mexico')
#plt.axis([x_A, x_B,  y_A, y_B])

plt.plot(X, Y,"o")
fig.savefig(PublicPATH+"/map.png")
