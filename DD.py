#!/usr/bin/env python3
from datetime import datetime
import glob
import xml.etree.ElementTree as ET
import mysql.connector
from mysql.connector import errorcode
import json

with open('db.json') as json_file:
    config = json.load(json_file)

try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = ("SELECT * FROM user")
    cursor.execute(query)

    for (name, lastname, age) in cursor:
        print("{0}, {1} was hired on {2}".format(name,lastname,age))

except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
    cnx.close()


PATH='home/quantics/public_html/static/'
for filename in glob.glob(PATH+"*.xml"):
    print(filename)
    tree = ET.parse(filename)
    root = tree.getroot()
    mydate =

#<places>
#  <place place_id="2039">
#    <name>ESTACION DE SERVICIO CALAFIA, S.A. DE C.V.</name>
#    <cre_id>PL/658/EXP/ES/2015</cre_id>
#    <location>
#      <x>-116.9214</x>
#      <y>32.47641</y>
#    </location>
#  </place>
#</places>
