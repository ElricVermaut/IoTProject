import pymongo as pymongo
from flask import Flask, request, jsonify
#from flask_objectid_converter import ObjectIDConverter
from pymongo import ReturnDocument
from pymongo.server_api import ServerApi
#from Schemas import TemperatureSensorSchema
from bson import json_util, ObjectId
#from flask_cors import CORS
import datetime as dt

# loading private connection information from environment variables
#from dotenv import load_dotenv

#load_dotenv()
import os

client = pymongo.MongoClient("mongodb+srv://Admin:admin@finalproject.oqgvx2z.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
db = client.test

# test line

# This is a test to check connection
if 'weather' not in db.list_collection_names():
    db.create_collection("weather",
                         timeseries={'timeField': 'timestamp', 'metaField': 'sensorId', 'granularity': 'minutes'})


# def print_hi(name):
#     print(f'Hi, {name}')
#
# if __name__ == '__main__':
#     print_hi('PyCharm')

