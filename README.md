Project Introduction:
For this project, we got the idea to make a device that will sense sound, temperature, and light to determine if the environmental conditions for sleeping are met. It will also record any drastic changes that may happen in the environment during sleep. This way, it will be possible to analyse sleep quality and provide interesting data to the user. The device will use an LCD module to display a message that will either tell you that the conditions are met or that there is too much sound, light, or too high or low temperature. All this data will be stored in the mongo database.
As for our target audience, anyone having trouble sleeping, or that is interested in finding out their sleep pattern may find use for our device.

Hardware design:
![image](https://user-images.githubusercontent.com/77856309/208313715-23966431-8aeb-4072-bba0-56d6a2f3f71d.png)

Sensors used:
Temperature sensor
Photoresistor
Big sound sensor
 

MongoDB Schema design proposal:

Data structure (JSON):
{
"Temperature.C": "24",
"Humidity": "Humid",
"Sound": "Silent",
"Light": "Dark",
“Adequate”: false,
“Date”: “12/11/2022 – 8:23”
}

API Endpoints
There are multiple ways to send requests to the api.

GET

http://127.0.0.1:5001/sensors/450/temperatures Returns 
{
    "measurementCount": 1,
    "sensorId": 450
}

http://127.0.0.1:5001/sensors/450/sounds Returns
{
    "measurementCount": 1,
    "sensorId": 450
}

POST
http://127.0.0.1:5001/sensors/450/ With params
{
    "temperature": 100,
    "humidity": "humid",
    "brightness": "bright",
    "sound": "quiet"
}
Returns
{
    "_id": "639f5be687205cb43680e5f7",
    "brightness": "bright",
    "humidity": "humid",
    "sensorId": 450,
    "sound": "quiet",
    "temperature": 100,
    "timestamp": "2022-12-18T13:28:54"
}
