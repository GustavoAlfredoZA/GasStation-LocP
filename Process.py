#!/usr/bin/env python3
import glob, os
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PATH='/home/quantics/public_html/static/'
os.chdir(PATH)
X=[]
Y=[]
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
        X.append(x)
        Y.append(y)
        #print(id,(x,y))


for file in glob.glob("*1.xml"):
    tree = ET.parse(file)
    root = tree.getroot()
    for place in root:
        id = place.get('place_id')
        for gas_price in place.iter('gas_price'):
            type=gas_price.attrib['type']
            price=gas_price.text
            #print(gas_price.attrib['type'],price)


fig = plt.figure()
ax = plt.subplots()
#ax.set(title='Gas Station Mexico')
#plt.axis([x_A, x_B,  y_A, y_B])
ax.grid()
ax.plot(X, Y,"o")
fig.savefig("/home/quantics/public_html/static/map.png")
#plt.plot(X,Y,"o")
#plt.savefig("/home/quantics/public_html/static/map.png")
