import mysql.connector
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import json

config_file = "config.json"
with open(config_file) as json_file:
    config = json.load(json_file)
    
# identifier for this station
STATION_NUMBER = 1
ACCESS_STATION_COUNTS = 3 + STATION_NUMBER

# connect to DB
cnx = mysql.connector.connect(**config)
cnx.set_charset_collation('utf8')
cursor = cnx.cursor()

rfid = SimpleMFRC522()

# poll for RFID tag read event
while True:
    id_number, text = rfid.read()

    # connect to database if RFID is read
    if id_number is not None:
        cursor.execute("SELECT * FROM audioobjs WHERE `id` = %s", "`"+str(id_number)+"`")    
        obj_metadata = cursor.fetchall()
        cursor.execute("SELECT * FROM mp3s WHERE `emotional_register` = %s", obj_metadata[0][1])
        possible_clips_metadata = cursor.fetchall()
        # perform storytelling decisions
        if len(possible_clips_metadata) > 1:
            pass

cursor.close()
cnx.close()