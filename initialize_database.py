import csv 
import mysql.connector
from enum import Enum, auto
import json

config_file = "config.json"
with open(config_file) as json_file:
    config = json.load(json_file)

# Enums can be used to guarantee data is standardized, if desired
class Scale(Enum):
    personal = auto()
    mit = auto()
    historical = auto()

class Timeline(Enum):
    before_MIT = auto()
    at_MIT = auto()
    after_MIT = auto()

# connect to database
cnx = mysql.connector.connect(**config)
cnx.set_charset_collation('utf8')
cursor = cnx.cursor()

# write SQL for generating the three tables
audio_object_table = (
    "CREATE TABLE `audioobjs` ("
    " `id` varchar(36) NOT NULL,"
    " `emotional_register` int(2) NOT NULL,"
    " `timeframe` varchar(100) NOT NULL,"
    " `scale` varchar(100) NOT NULL,"
    " `count1` int(16) DEFAULT 0,"
    " `count2` int(16) DEFAULT 0,"
    " `count3` int(16) DEFAULT 0,"
    " PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB charset=utf8"
)

mp3_table = (
    "CREATE TABLE `mp3s` ("
    " `id` varchar(36) NOT NULL,"
    " `emotional_register` int(2) NOT NULL,"
    " `timeframe` varchar(100) NOT NULL,"
    " `scale` varchar(100) NOT NULL,"
    " `count1` int(16) DEFAULT 0,"
    " `count2` int(16) DEFAULT 0,"
    " `count3` int(16) DEFAULT 0,"
    " PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB charset=utf8"   
)

interviewee_table = (
    "CREATE TABLE `interviewees` ("
    " `name` varchar(36) NOT NULL,"
    " `affiliation` varchar(1000) NOT NULL,"
    " `grad_year` int(4) DEFAULT NULL,"
    " `major` varchar(1000) DEFAULT NULL,"
    " `race` varchar(1000) NOT NULL,"
    " `count1` int(16) DEFAULT 0,"
    " `count2` int(16) DEFAULT 0,"
    " `count3` int(16) DEFAULT 0,"
    " PRIMARY KEY (`name`)"
    ") ENGINE=InnoDB charset=utf8"  
)

# run if no table has yet been created
print("creating table")
cursor.execute(audio_object_table)
cursor.execute(mp3_table)
cursor.execute(interviewee_table)

# SQL command for adding an audio object to the table
add_audio_object = ("INSERT INTO audioobjs "
               "(id, emotional_register, timeframe, scale) "
               "VALUES (%s, %s, %s)")

with open('audio_clips.csv') as csvfile:
    reader = csv.reader(csvfile)
    for i, row in enumerate(reader):
        clip_data = tuple(row)
        try:
            cursor.execute(add_audio_object, clip_data)
            cnx.commit()
        except Exception as err:
            print(err)

cursor.close()
cnx.close()