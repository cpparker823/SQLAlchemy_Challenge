# Import the dependencies.
import numpy as np
import datetime as dt
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()

# reflect the tables
base.prepare(autoload_with=engine)


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
    precipitation = dict(results)
    session.close()
    return jsonify(precipitation)

#Stations
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(station.station).all()
    station_list = [station[0] for station in results]
    session.close()
    return jsonify(station_list)

#Temperature Observed
@app.route("/api/v1.0/tobs")
def tobs():
     session = Session(engine)
     prev_year_date = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
     result = session.query(Measurement.tobs).\
        filter(Measurement.station=='USC00519281').\
        filter(Measurement.date >= prev_year_date).all()
     waihee = list(np.ravel(result))
     session.close()
     return jsonify(waihee)

#Minimum, maximum, and average temps by start date
@app.route("/api/v1.0/<start>")
def temp_starts(start):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs) ,func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= prev_year_date).all()
    session.close()

    temps = []
    for result in results:
        temps_list = {
            "Min": result[0],
            "Avg": result[1],
            "Max": result[2]
        }
        temps.append(temps_list)
    return jsonify(temps)



if __name__ == '__main__':
    app.run()









