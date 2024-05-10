# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask
import sqlite3


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///C:\Repos\SurfsUp_Hawaii_Weather\Starter_Code\Resources\hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()

# reflect the tables
base.prepare(autoload_with=engine, reflect = True)

# Save references to each table
station = base.classes.station
measurement = base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

#List all routes
@app.route("/")
def welcome():
    return (
        f"Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
)

#Precipitation by date
@app.route("/api.v1.0/precipitation")
def precipitation():
    session = Session(engine)
    prev_year_date = dt.date(2017,8,23) - (dt.timedelta(days = 365))
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= prev_year_date).all()
    session.close()
    precipitation = dict(results)
    return jsonify(precipitation)