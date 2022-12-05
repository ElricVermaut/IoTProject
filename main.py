#import ISODate as ISODate
import pymongo as pymongo
#from flask import Flask, request, jsonify
#from flask_objectid_converter import ObjectIDConverter
#from pymongo import ReturnDocument
from pymongo.server_api import ServerApi
#from Schemas import TemperatureSensorSchema
from bson import json_util, ObjectId
#from flask_cors import CORS
from datetime import datetime, tzinfo, timezone
# loading private connection information from environment variables
#from dotenv import load_dotenv

#load_dotenv()
import os

client = pymongo.MongoClient("mongodb+srv://Admin:admin@finalproject.oqgvx2z.mongodb.net/?retryWrites=true&w=majority",
                             server_api=ServerApi('1'))
db = client.test

# test line

# This is a test to check connection
if 'Environment' not in db.list_collection_names():
    db.create_collection("Environment",
                         timeseries={'timeField': 'timestamp', 'metaField': 'sensorId', 'granularity': 'minutes'})

# Insert dummy data
db.Environment.insert_one({
    "timestamp": datetime.now(),
    "sensorId": 450,
    "temperature": 70,
    "humidity": 'humid',
    "brightness": 'bright',
    "sound": 'quiet'
  })

db.Environment.aggregate([{
    '$match': {
         'timestamp': {
           '$gte': datetime.now()-1,
            '$lt': datetime.now()
        }
    }
}, {
    '$group': {
        '_id': {
            '$dateToString': {
                'format': '%Y-%m-%dT%H',
                'date': '$timestamp'
            }
        },
        'averageTemp': {
            '$avg': '$temperature'
        }
    }
}, {
    '$sort': {
        'timestamp': 1
    }
}])

db.Environment.aggregate([{
        '$match': {
            'timestamp': {
                '$gte': datetime.now()-1,
                '$lt': datetime.now()
            }
        }
    }, {
        '$group': {
            '_id': '$humidity',
            'measurementCount': {
                '$count': {}
            }
        }
    }, {
        '$sort': {
            'humidity': -1
        }
    }
])