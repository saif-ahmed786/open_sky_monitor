from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import os

app = FastAPI()
scheduler = BackgroundScheduler()

OPEN_SKY_URL = "https://opensky-network.org/api/states/all"

OPEN_SKY_URL_Frankfurt = "https://opensky-network.org/api/states/all?lamin=49.9&lomin=8.4&lamax=50.2&lomax=8.7"

def fetch_opensky():
    print("fetching data from api...")
    response = requests.get(OPEN_SKY_URL,timeout=10)
    if response.status_code == 200:
        print("satus 200")
        data = response.json()
        if "states" in data:
            for state in data["states"][:50]:  # limit for demo
                record = {
                    "icao24": state[0],
                    "callsign": state[1],
                    "lat": state[6],
                    "lon": state[5],
                    "velocity": state[9],
                    "timestamp": data["time"]
                }
                print(record)
        
    else:
        print("api not working", response)


@app.get("/")
def root():
    return {"message":"Real-time of Open Sky Tracking"}

