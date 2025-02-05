# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table

Station=Base.classes.station
Measurement=Base.classes.measurement

# Create our session (link) from Python to the DB
session=Session(engine)

#################################################
# Flask Setup
#################################################
app=Flask(__name__)



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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"

        f"The date format must be input as dd-mm-yyyy, for example 31-12-2010"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    

    """Return a json representation of the dictionary of results from precipitation analysis"""
    # Find the most recent date in the data set.
    recent_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    #Getting the recent date from the tuple and converting it into datetime
    recent_date_dt=dt.datetime.strptime(recent_date[0], '%Y-%m-%d')
    recent_date_date=recent_date_dt.date()

      
    # Calculate the date one year from the last date in data set.
    date_one_year_ago=recent_date_date-dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    data=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=date_one_year_ago).all()

    session.close()


    # Convert data into dictionary using dictionary comprehension
    prcp_dict={date: prcp for date, prcp in data}
   
   #Return the json representation of the prcp_dictionary
    return jsonify(prcp_dict)




@app.route("/api/v1.0/stations")
def stations():
    
    """Return a json list of stations from the dataset"""
    # Query to get stations 
    station_data = session.query(Station.station).all()

    session.close()

    # Create a list containing stations name
    station_names = list(np.ravel(station_data))
    
    return jsonify(station_names)


@app.route("/api/v1.0/tobs")
def tobs():
    
    """Query and the dates and temperature observations of the most-active stations for the previous year data"""

    # Query to get dates and temperature observations of the most-active station for the previous year 
    
    active_stations=session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).\
                                                    order_by(func.count(Measurement.station).desc()).all()
    
    active_id=active_stations[0][0]

    active_date_and_temp=session.query(Measurement.date, Measurement.tobs).filter(Measurement.station==active_id).all()


    session.close()
    
    # Create a list containing temperatures from active stations by appending temperature from tuple
    active_temp_list=[]
    for entry in active_date_and_temp:
        active_temp_list.append(entry[1])



    # Return a json list of temperatures

    return jsonify(active_temp_list)



@app.route("/api/v1.0/<start>")
def temp_start(start):
    """Return a JSON list of the min, avg, and max temperatures for a given start date"""
    session = Session(engine)

    try:
        # Ensure the start date is in the correct format
        start = dt.datetime.strptime(start, "%d-%m-%Y")

    except ValueError:
        return jsonify({"error": "Invalid date format. Use DD-MM-YY."}), 400

    # Query to get min, avg, and max temperatures from the given start date
    temp_para = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).all()

    session.close()
    
    temp_result = {
        "Start Date": start,
        "Min Temperature": temp_para[0][0],
        "Avg Temperature": temp_para[0][1],
        "Max Temperature": temp_para[0][2]
    }

    return jsonify(temp_result)



@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):
    """Return a JSON list of the min, avg, and max temperatures for a given start-end range."""
    session = Session(engine)

    try:
        # Ensure the start date is in the correct format
        start = dt.datetime.strptime(start, "%d-%m-%Y")
        end = dt.datetime.strptime(end, "%d-%m-%Y")

    except ValueError:
        return jsonify({"error": "Invalid date format. Use DD-MM-YY."}), 400


    # Query to get min, avg, and max temperatures within the date range
    temp_para_2 = session.query(func.min(Measurement.tobs),
                              func.avg(Measurement.tobs),
                              func.max(Measurement.tobs)).\
                              filter(Measurement.date >= start).\
                              filter(Measurement.date <= end).all()

    session.close()

    temp_result_2 = {
        "Start Date": start,
        "End Date": end,
        "Min Temperature": temp_para_2[0][0],
        "Avg Temperature": temp_para_2[0][1],
        "Max Temperature": temp_para_2[0][2]
    }

    return jsonify(temp_result_2)



if __name__ == '__main__':
    app.run(debug=True)