#!/usr/bin/env python3
import glob, os
import xml.etree.ElementTree as ET
import numpy as np
import json
import mysql.connector
from mysql.connector import errorcode
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from pprint import pprint
from shapely.geometry import MultiPolygon, Polygon
import shapely.geometry as sg
import shapely.ops as so
import subprocess

p = open("routes.json")
routes = json.load(p)
ProyectPATH=routes['proyect']
PublicPATH=routes['public']
p.close()

with open('db.json') as json_file:
    config = json.load(json_file)

with open('mexicostatesprod.json') as statesgeojson:
    states = json.load(statesgeojson)

allStates=[]
for state in states['features']:
    if(len(state['geometry']['coordinates'][0])>1):
        Estado = Polygon([(i[0],i[1]) for i in state['geometry']['coordinates'][0]])

    else:
        Estado=MultiPolygon([Polygon([[(c[0],c[1]) for c in p] for p in m][0]) for m in state['geometry']['coordinates']])

    allStates.append([Estado,state['properties']['postal']])


def searchstate(x,y,allStates):
    place=Point(y,x)
    for state in allStates:
        if(state[0].contains(Point(x,y))):
            return(state[1])

try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    updatestates = "INSERT INTO pricesTime(statec,number,datec,priceregular,pricepremium,pricediesel,nregular,npremium,ndiesel) SELECT tmp.state, tmp.numberplaces ,tmp. today, tmp.pricer, tmp.pricep, tmp.pricep, tmp.numberr, tmp.numberp, tmp.numberd FROM ( SELECT places.state AS state, COUNT(*) AS numberplaces, CURDATE() AS today, SUM(regular) AS pricer, SUM(premium) AS pricep, SUM(diesel) AS priced, COUNT(regular) AS numberr, COUNT(premium) AS numberp, COUNT(diesel) AS numberd FROM places LEFT JOIN prices ON places.place_id = prices.prices_place_id WHERE state is not null GROUP BY places.state ) AS tmp ON DUPLICATE KEY UPDATE priceregular = tmp.pricer, pricepremium = tmp.pricep, pricediesel = tmp.priced, nregular = tmp.numberr, npremium = tmp.numberp, ndiesel = tmp.numberd"
    cursor.execute(updatestates)
    query1 = ("INSERT INTO places(place_id,name,cre_id,x,y,state) VALUES (%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE name = %s , cre_id = %s , x = %s , y = %s , state = %s ")
    queryr = ("INSERT INTO prices( prices_place_id , regular ) VALUES ( %s , %s ) ON DUPLICATE KEY UPDATE regular = %s ")
    queryp = ("INSERT INTO prices( prices_place_id , premium ) VALUES ( %s , %s ) ON DUPLICATE KEY UPDATE premium = %s ")
    queryd = ("INSERT INTO prices( prices_place_id , diesel ) VALUES ( %s , %s ) ON DUPLICATE KEY UPDATE diesel = %s ")

    os.chdir(ProyectPATH)
    for file in glob.glob("*0.xml"):
        tree = ET.parse(file)
        root = tree.getroot()
        for GasStation in root:

            id = GasStation.get('place_id')
            name = GasStation.find('name').text
            cre_id = GasStation.find('cre_id').text
            location = GasStation.find('location')
            x = location.find('x').text
            y = location.find('y').text
            state = searchstate(float(x),float(y),allStates)
            data_query = ( id , name , cre_id , x , y , state , name , cre_id , x , y , state)
            cursor.execute(query1,data_query)


    for file in glob.glob("*1.xml"):
        tree = ET.parse(file)
        root = tree.getroot()
        for place in root:
            id = place.get('place_id')
            P = [0,0,0]
            for gas_price in place.iter('gas_price'):

                type = gas_price.attrib['type']
                price = gas_price.text
                data_query2 = (id,price,price)
                if(type == 'regular'):
                    query2 = queryr
                elif(type == 'premium'):
                    query2 = queryp
                else:
                    query2 = queryd

                cursor.execute(query2,data_query2)


    cnx.commit()
    subprocess.call("mv *.xml backup/", shell=True)

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cnx.close()
