from marshmallow import Schema, fields, validate

class SensorSchema(Schema):
    #timestamp = fields.DateTime(required=True)
    temperature = fields.Number(required=True)
    brightness = fields.String(required=True)
    sound = fields.String(required=True)
    humidity = fields.String(required=True)