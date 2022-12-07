
import pymongo as pymongo
from flask import Flask, request, jsonify
from flask_objectid_converter import ObjectIDConverter
from pymongo import ReturnDocument
from pymongo.server_api import ServerApi
from Schemas import SensorSchema
from bson import json_util, ObjectId
from flask_cors import CORS
from datetime import datetime, timedelta

# loading private connection information from environment variables
from dotenv import load_dotenv

load_dotenv()
import os

client = pymongo.MongoClient("mongodb+srv://Admin:admin@finalproject.oqgvx2z.mongodb.net/?retryWrites=true&w=majority",
                             server_api=ServerApi('1'))
db = client.test

# test line

# This is a test to check connection
if 'Environment' not in db.list_collection_names():
    db.create_collection("Environment",
                         timeseries={'timeField': 'timestamp', 'metaField': 'sensorId', 'granularity': 'minutes'})

def getTimeStamp():
    return datetime.datetime.today().replace(microsecond=0)

app = Flask(__name__)
app.url_map.converters['objectid'] = ObjectIDConverter

app.config['DEBUG'] = True
# making our API accessible by any IP
CORS(app)

@app.route("/sensors/<int:sensorId>/", methods=["POST"])
def add_value(sensorId):
    error = SensorSchema().validate(request.json)
    if error:
        return error, 400

    data = request.json
    data.update({"timestamp": getTimeStamp(), "sensorId": sensorId})

    db.weather.insert_one(data)

    data["_id"] = str(data["_id"])
    data["timestamp"] = data["timestamp"].strftime("%Y-%m-%dT%H:%M:%S")
    # Insert dummy data
    """
    db.Environment.insert_one({
        "timestamp": datetime.now(),
        "sensorId": 450,
        "temperature": 70,
        "humidity": 'humid',
        "brightness": 'bright',
        "sound": 'quiet'
    })
    """
    return data

@app.route("/sensors/<int:sensorId>/temperatures")
def get_all_temperatures(sensorId):
    start = request.args.get("start")
    end = request.args.get("end")

    query = {"sensorId": sensorId}
    if start is None and end is not None:
        try:
            end = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400

        query.update({"timestamp": {"$lte": end}})

    elif end is None and start is not None:
        try:
            start = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400

        query.update({"timestamp": {"$gte": start}})
    elif start is not None and end is not None:
        try:
            start = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
            end = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")

        except Exception as e:
            return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400

        query.update({"timestamp": {"$gte": start, "$lte": end}})

    #sortedTemperatureData = list(

    data = list(
        db.Environment.aggregate([{
            '$match': {
                'timestamp': {
                    '$gte': datetime.now() - timedelta(days=1),
                    '$lte': datetime.now()

                }
            }
        }, {
            '$group': {
                '_id': '$temperature',
                'measurementCount': {
                    '$count': {}
                }
            }
        }, {
            '$sort': {
                'temperature': 1
            }
        }
        ]))

    if data:
        data = data[0]
        if "_id" in data:
            del data["_id"]
            data.update({"sensorId": sensorId})

        for temp in data['temperatures']:
            temp["timestamp"] = temp["timestamp"].strftime("%Y-%m-%dT%H:%M:%S")

        return data
    else:
        return {"error": "id not found"}, 404


if __name__ == "__main__":
    app.run(port=5001)

dailyData  = list(
db.Environment.aggregate([{
    '$match': {
         'timestamp': {
           '$gte': datetime.now() - timedelta(days=1),
            '$lte': datetime.now()

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
        '_id': 1
    }
}]))
sortedHumidityData  = list(
db.Environment.aggregate([{
        '$match': {
            'timestamp': {
'$gte': datetime.now() - timedelta(days=1),
'$lte': datetime.now()

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
            'humidity': 1
        }
    }
]))
sortedSoundData  = list(
db.Environment.aggregate([{
    '$match': {
        'timestamp': {
            '$gte': datetime.now() - timedelta(days=1),
            '$lte': datetime.now()
        }
    }
}, {
    '$group': {
        '_id': '$sound',
        'measurementCount': {
            '$count': {}
        }
    }
}, {
    '$sort': {
        'sound': -1
    }
}
]))
sortedTemperatureData  = list(
db.Environment.aggregate([{
        '$match': {
            'timestamp': {
'$gte': datetime.now() - timedelta(days=1),
'$lte': datetime.now()

            }
        }
    }, {
        '$group': {
            '_id': '$temperature',
            'measurementCount': {
                '$count': {}
            }
        }
    }, {
        '$sort': {
            'temperature': 1
        }
    }
]))
sortedBrightnessData  = list(
db.Environment.aggregate([{
        '$match': {
            'timestamp': {
                '$gte': datetime.now() - timedelta(days=1),
                '$lte': datetime.now()
            }
        }
    }, {
        '$group': {
            '_id': '$brightness',
            'measurementCount': {
                '$count': {}
            }
        }
    }, {
        '$sort': {
            'brightness': 1
        }
    }
]))
print("Daily Data:")
print(dailyData)
print("Sort by humidity:")
print(sortedHumidityData)
print("Sort by sound:")
print(sortedSoundData)
print("Sort by temperature:")
print(sortedTemperatureData)
print("Sort by brightness:")
print(sortedBrightnessData)
