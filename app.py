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

# define variables for start and end date
session = Session(engine)

most_recent_date = Session.query(measurement.date).order_by(measurement.date.desc()).first()
one_year_from_start = dt.date(2017,8,23) - dt.timedelta(days=365)

session.close()


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
        f"Temperature Stat from Start Date (yyyy-mm-dd): /api/v1.0/yyyy-mm-dd<br/>"
        f"Temperature Stat from Start to End Date (yyyy-mm-dd): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
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
    session = Session(engine)

    results = session.query(measurement.tobs, measurement.date).filter(measurement.date >= one_year_from_start)

    session.close()

    tobs = []
    for tobs, date in results:
        tobs_dict = {}
        tobs_dict["Tobs"] = tobs
        tobs_dict["Date"] = date
        tobs.append(tobs_dict)

    return jsonify(tobs)




if __name__ == '__main__':
    app.run(debug=True)