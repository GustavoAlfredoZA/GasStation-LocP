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
    query=("SELECT places.place_id,places.name,places.cre_id,places.x,places.y,prices.regular,prices.premium,prices.diesel FROM places LEFT JOIN prices ON places.place_id = prices.prices_place_id")
    cursor.execute(query)
    for a in cursor:
        print(type(a))
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cnx.close()
