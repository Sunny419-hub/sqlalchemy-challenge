import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    # Query all date and PRCP
    measurement = Base.classes.measurement
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()

    # Convert the query results to a dictionary using date as the key and prcp as the value
   
    all_precipitation = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        all_precipitation.append(prcp_dict)

    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")

def stations():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    # Query stations
    station = Base.classes.station
    results = session.query(station.station).all()

    session.close()
    return jsonify(results)


@app.route("/api/v1.0/tobs")
def tobs():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query tobs
    measurement = Base.classes.measurement
    
    # Query the last 12 months of temperature observation data for this station
    year_ago = dt.date(2017,8,18) - dt.timedelta(days=365)
    results = session.query(measurement.tobs).\
        filter(measurement.date >= year_ago).\
        filter(measurement.station == "USC00519281").all()
     
    session.close()
    return jsonify(results)
    

@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    measurement = Base.classes.measurement
    
    # Query start date
    results = session.query( 
                            func.avg(measurement.tobs), 
                            func.max(measurement.tobs), 
                            func.min(measurement.tobs)).\
                    filter(measurement.date >= start).all()
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_start = []
    for avg, maxi, mini in results:
        start_dict = {}
        start_dict["avg"] = avg
        start_dict["maxi"] = maxi
        start_dict["mini"] = mini
        all_start.append(start_dict)

    return jsonify(all_start)

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    measurement = Base.classes.measurement
    
    # Query all passengers
    results = session.query( 
                            func.avg(measurement.tobs), 
                            func.max(measurement.tobs), 
                            func.min(measurement.tobs)).\
                            filter(measurement.date >= start).filter(measurement.date <= end).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_start_end = []
    for avg, maxi, mini in results:
        start_end_dict = {}
        start_end_dict["avg"] = avg
        start_end_dict["maxi"] = maxi
        start_end_dict["mini"] = mini
        all_start_end.append(start_end_dict)

    return jsonify(all_start_end)

if __name__ == '__main__':
    app.run(debug=True)
