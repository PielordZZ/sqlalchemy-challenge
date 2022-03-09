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

begin_date = last_date - dt.timedelta(days=365)

#Flask Routes


#Home

@app.route('/')
def home():
    #documentation
    return('''Queries follow following formats \n\n\n 
    /api/v1.0/precipitation  -provide dictionary of all preceipitation data by date\n
    /api/v1.0/stations  -list all stations\n
    /api/v1.0/tobs  -list of last year's Temperature data\n
    /api/v1.0/<yyyy-mm-dd>  -min, max and average temperature after that day\n
    /api/v1.0/<yyyy-mm-dd>/<yyyy-mm-dd>  -min, max and average temperature between those days''')


@app.route('/api/v1.0/precipitation')
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)


    # Query all precip info
    results = session.query(Measurement.prcp,Measurement.date).all()

    session.close()

    precip_data = {}
    for m in results:
        precip_data[m[1]] =m[0]

    print(precip_data)
    return(jsonify(precip_data))

@app.route('/api/v1.0/stations')
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)


    # Query distinct stations
    results = session.query(Measurement.station.distinct()).all()

    session.close()
    stationlist = []
    for s in results:
        stationlist.append(s[0])
    return(jsonify(stationlist))


@app.route('/api/v1.0/tobs')
def tobs():

    # Create our session (link) from Python to the DB
    session = Session(engine)


    # Query list of temperatures for 1 year
    
    results = session.query(Measurement.tobs).filter(Measurement.date >= begin_date).filter(Measurement.date <=last_date).order_by(Measurement.date).all()

    session.close()
    temps = []
    for s in results:
        temps.append(s[0])
    return(jsonify(temps))

@app.route('/api/v1.0/<startdate>')
def tempstatssimple(startdate):

    # Create our session (link) from Python to the DB
    session = Session(engine)


    # Query list of temperatures for 1 year
    
    results = session.query(func.avg(Measurement.tobs),func.min(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= startdate)

    session.close()
    return(jsonify([results[0][0],results[0][1],results[0][2]]))
@app.route('/api/v1.0/<startdate>/<enddate>')
def tempstats(startdate,enddate):

    # Create our session (link) from Python to the DB
    session = Session(engine)


    # Query list of temperatures for 1 year
    
    results = session.query(func.avg(Measurement.tobs),func.min(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= startdate).filter(Measurement.date < enddate)

    session.close()
    return(jsonify([results[0][0],results[0][1],results[0][2]]))
if __name__ == '__main__':
    app.run(host= 'localhost',port =5000,debug=True)