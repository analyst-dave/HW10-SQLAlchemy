########
# instruction for Step 2 - Climate App from the HW README.md is so short(2 short sentences for each api) need major clarification, 
# confusing, and lack of elaboration... for example, "Convert the query results to a dictionary using date as the key and prcp as the value"
# What query results is it talking about? use pandas/alchemy/session/engine/read_sql/read_csv? Any extra condition(filter)? sorting direction?
# I did NOT enjoy this Flask App part at all mainly due to the lack of explaination/elaborating on instructions
# very confusing and forced us to make all sorts of assumptions, which might increase time spent significantly... very upset & frustrated
########

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt

app = Flask(__name__)


@app.route("/")
def welcome():
    print("landing...")
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
        f"/about"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'precipitation' page...")
    
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    conn = engine.connect()
    data_df = pd.read_sql("SELECT date, sum(prcp) FROM measurement group by date", conn)
    print(data_df)
  
    dict1 = {}
    for index, row in data_df.iterrows():
        dict1[row['date']] = row['sum(prcp)']
        #print(row)
    
    return jsonify(dict1)

@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'stations' page...")

    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    # list all records from 'station' table
    data = engine.execute("SELECT station  FROM station")
  
    li1 = []
    for record in data:
        li1.append(record[0])
        print(record[0])
    
    return jsonify(li1)

@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'tobs' page...")

    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    conn = engine.connect()
    data_df = pd.read_sql("SELECT date, tobs FROM measurement where station == 'USC00519281' and date >= '2016-08-23'", conn)
    print(data_df)
  
    li1 = []
    for index, row in data_df.iterrows():
        li1.append(row['tobs'])
    
    return jsonify(li1)

@app.route("/api/v1.0/<start>")
def start(start):
    print("Server received request for '<start>' page...")
    print(start)
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    conn = engine.connect()
    data_df = pd.read_sql(f"SELECT date, min(tobs), max(tobs), avg(tobs) FROM measurement where date >= {start}", conn)
    print(data_df)
    
    dict1 = {}
    for index, row in data_df.iterrows():
        dict1[start] = start
        dict1['min'] = row['min(tobs)']
        dict1['max'] = row['max(tobs)']
        dict1['avg'] = row['avg(tobs)']
    return jsonify(dict1)

@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    print("Server received request for '<start>/<end>' page...")
    print(start)
    print(end)
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    conn = engine.connect()
    data_df = pd.read_sql(f"SELECT date, min(tobs), max(tobs), avg(tobs) FROM measurement where date >= {start} and date <= {end}", conn)
    
    dict1 = {}
    for index, row in data_df.iterrows():
        dict1[start] = end
        dict1['min'] = row['min(tobs)']
        dict1['max'] = row['max(tobs)']
        dict1['avg'] = row['avg(tobs)']
    return jsonify(dict1)

@app.route("/about")
def about():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page..."

if __name__ == "__main__":
    app.run(debug=True)
