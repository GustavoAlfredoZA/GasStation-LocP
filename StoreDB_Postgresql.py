#!/usr/bin/env python3
import glob, os
import xml.etree.ElementTree as ET
import numpy as np
import json
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from pprint import pprint
from shapely.geometry import MultiPolygon, Polygon
import shapely.geometry as sg
import shapely.ops as so
import subprocess
import psycopg2
import urllib3

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
    config = os.getenv('DATABASE_URL', 'postgresql:///gasstationdb')
    cnx = psycopg2.connect(config)
    cursor = cnx.cursor()
    updatestates = "INSERT INTO pricesTime(statec,number,datec,priceregular,pricepremium,pricediesel,nregular,npremium,ndiesel) SELECT tmp.state, tmp.numberplaces ,tmp. today, tmp.pricer, tmp.pricep, tmp.pricep, tmp.numberr, tmp.numberp, tmp.numberd FROM ( SELECT places.state AS state, COUNT(*) AS numberplaces, TIMEZONE('America/Mexico_City',NOW())::DATE AS today, SUM(regular) AS pricer, SUM(premium) AS pricep, SUM(diesel) AS priced, COUNT(regular) AS numberr, COUNT(premium) AS numberp, COUNT(diesel) AS numberd FROM places LEFT JOIN prices ON places.place_id = prices.prices_place_id WHERE state is not null GROUP BY places.state ) AS tmp ON CONFLICT (statec,datec) DO UPDATE SET priceregular = EXCLUDED.priceregular, pricepremium = EXCLUDED.pricepremium, pricediesel = EXCLUDED.pricediesel, nregular = EXCLUDED.nregular, npremium = EXCLUDED.npremium, ndiesel = EXCLUDED.ndiesel"
    cursor.execute(updatestates)
    query1 = ("INSERT INTO places(place_id,name,cre_id,x,y,state) VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT (place_id) DO UPDATE SET name = %s , cre_id = %s , x = %s , y = %s , state = %s ")
    queryr = ("INSERT INTO prices( prices_place_id , regular ) VALUES ( %s , %s ) ON CONFLICT ( prices_place_id ) DO UPDATE SET regular = %s ")
    queryp = ("INSERT INTO prices( prices_place_id , premium ) VALUES ( %s , %s ) ON CONFLICT ( prices_place_id ) DO UPDATE SET premium = %s ")
    queryd = ("INSERT INTO prices( prices_place_id , diesel ) VALUES ( %s , %s ) ON CONFLICT ( prices_place_id ) DO UPDATE SET diesel = %s ")

    http = urllib3.PoolManager()
    places = http.request('GET', 'https://publicacionexterna.azurewebsites.net/publicaciones/places')
    tree = ET.parse(places.data)
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

    http = urllib3.PoolManager()
    prices = http.request('GET', 'https://publicacionexterna.azurewebsites.net/publicaciones/prices')
    tree = ET.parse(prices.data)
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
    
except psycopg2.Error as err:
    print(err)
else:
    cnx.close()
