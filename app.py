# import dependencies
import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# import Flask and jsonify
from flask import Flask, jsonify

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()

# reflect the tables
base.prepare(engine, reflect=True)

# Save references to each table
measurement = base.classes.measurement
station = base.classes.station

# flask set up
app = Flask(__name__)

# set up routes

# home page route

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"Stations: /api/v1.0/stations<br/>"
        f"Tobs: /api/v1.0/tobs<br/>"
        f"Temperature Stats from Start Date (yyyy-mm-dd): /api/v1.0/yyyy-mm-dd<br/>"
        f"Temperature Stats from Start to End Date (yyyy-mm-dd): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )

# precipitation route

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    select = [measurement.date, measurement.prcp]
    result = session.query(*select).all()
    session.close()

    precipitation = []
    for date, prcp in result:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        precipitation.append(prcp_dict)
        
    return jsonify(precipitation)

# stations route

@app.route("/api/v1.0/stations")
def stations():
    station = base.classes.station
    session = Session(engine)
    select = [station.station, station.name, station.latitude, station.longitude, station.elevation]
    result = session.query(*select).all()
    session.close()

    stations = []
    for station, name, latitude, longitude, elevation in result:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Latitude"] = latitude
        station_dict["Longitude"] = longitude
        station_dict["Elevation"] = elevation
        stations.append(station_dict)
        
    return jsonify(stations)

# tobs route

@app.route('/api/v1.0/tobs')
def tobs():
    measurement = base.classes.measurement
    session = Session(engine)

    one_year_from_start = dt.date(2017,8,23) - dt.timedelta(days=365)
    result = session.query(measurement.tobs, measurement.date).filter(measurement.date >= one_year_from_start).all()

    session.close()

    tobs_list = []
    for tobs, date in result:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

# start date route

@app.route('/api/v1.0/<start>')
def start(start):
    session = Session(engine)

    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
            filter(measurement.date >= start).group_by(measurement.date).all()

    start_tobs_list = []
    for min, max, avg in results:
        start_tobs_dict = {}
        start_tobs_dict["Minimum Temperature"] = min
        start_tobs_dict["Maximum Temperature"] = max
        start_tobs_dict["Average Temperature"] = avg
        start_tobs_list.append(start_tobs_dict)

    session.close()

    return jsonify(start_tobs_list)

# start/end date route

@app.route('/api/v1.0/<start><end>')
def start_end(start,end):
    measurement = base.classes.measurement
    session = Session(engine)

    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
            filter(measurement.date >= start).filter(measurement.date <= end).group_by(measurement.date).all()

    start_end_list = []
    for min, max, avg in results:
        start_end_dict = {}
        start_end_dict["Minimum Temperature"] = min
        start_end_dict["Maximum Temperature"] = max
        start_end_dict["Average Temperature"] = avg
        start_end_list.append(start_end_dict)

    session.close()

    return jsonify(start_end_list)


if __name__ == '__main__':
    app.run(debug=True)