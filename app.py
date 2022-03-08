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
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement


#flask init
app = Flask(__name__)

#global variables

session = Session(engine)
last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
last_date = dt.date.fromisoformat(last_date[0])

session.close()
#Flask Routes


#Home

@app.route('/')
def home():
    #documentation
    return(
        f'Queries follow following formats \n'
        f"/api/v1.0/precipitation  -provide dictionary of all preceipitation data by date"
        f'/api/v1.0/stations  -list all stations'
        f"/api/v1.0/tobs  -list of last year's Temperature data"
        f'/api/v1.0/<yyyy-mm-dd>  -min, max and average temperature after that day'
        f'/api/v1.0/<yyyy-mm-dd>/<yyyy-mm-dd>  -min, max and average temperature between those days'
    
    )


@app.route('/api/v1.0/precipitation')
def prcp():


    return()