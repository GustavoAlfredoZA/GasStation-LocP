#!/usr/bin/env python3
import glob, os
import xml.etree.ElementTree as ET
import numpy as np
import json
import mysql.connector
from mysql.connector import errorcode

p = open("routes.json")
routes = json.load(p)
ProyectPATH=routes['proyect']
PublicPATH=routes['public']
p.close()

with open('db.json') as json_file:
    config = json.load(json_file)



try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query1 = ("INSERT INTO places(place_id,name,cre_id,x,y) VALUES (%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE name = %s , cre_id = %s , x = %s , y = %s ")
    queryr = ("INSERT INTO prices( prices_place_id , regular ) VALUES ( %s , %s ) ON DUPLICATE KEY UPDATE regular = %s ")
    queryp = ("INSERT INTO prices( prices_place_id , premium ) VALUES ( %s , %s ) ON DUPLICATE KEY UPDATE premium = %s ")
    queryd = ("INSERT INTO prices( prices_place_id , diesel ) VALUES ( %s , %s ) ON DUPLICATE KEY UPDATE diesel = %s ")

    os.chdir(PublicPATH)
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
            data_query = ( id , name , cre_id , x , y , name , cre_id , x , y )
            cursor.execute(query1,data_query)


    for file in glob.glob(PublicPATH+"*1.xml"):
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

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cnx.close()
