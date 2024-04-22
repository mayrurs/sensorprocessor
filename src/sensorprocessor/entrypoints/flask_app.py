from flask import Flask, request, jsonify

from datetime import datetime

from sensorprocessor.adapters import orm
from sensorprocessor.domain import commands
from sensorprocessor.service_layers import unit_of_work, messagebus
from sensorprocessor import views

app = Flask(__name__)

orm.start_mappers()

@app.route("/")
def healthcheck():
    return "Sensorprocessor API is working fine"

@app.route("/sensordata/<sensor>", methods=["GET"])
def sensordata(sensor):
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    result = views.sensordata(sensor, uow)
    return jsonify(result, 200)

@app.route("/add_rawdata/", methods=["POST"])
def add_rawdata():
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    time_format =  '%Y-%m-%d %H:%M:%S'
    cmd = commands.CreateRawData(
            request.json["sensor"],
            request.json["value"],
            datetime.strptime(request.json["timestamp"], time_format)
            )
    messagebus.handle(cmd, uow)
    return "OK", 201

@app.route("/get_current_value/<sensor>", methods=["GET"])
def get_current_value(sensor):
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    result = views.get_current_value(sensor, uow)
    print(result)
    if not result:
        return "not found", 404
    return jsonify(result), 200



