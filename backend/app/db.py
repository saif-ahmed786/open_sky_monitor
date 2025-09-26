import os
import psycopg2
from influxdb_client import InfluxDBClient, Point, WritePrecision


PG_CONN = psycopg2.connect(dbname="app", user="app", password ="temp1234",host = "postgres")
PG_CUR = PG_CONN.cursor()

#creat table 
PG_CUR.execute("""
               CREAT TABLE IF NOT EXIST FLIGHTS (
               icao24 TEXT,
               callsign TEXT,
               lat DOUBLE PRECISION,
               lon DOUBLE PRECISION,
               velocitz DOUBLE PRECISION,
               ts BIGINT);""")

PG_CONN.commit()

#influxdb connect

INFLUX_URL = os.getenv("INFLUX_URL", "http://influxdb:8086")

client = InfluxDBClient(
    url = INFLUX_URL,
    token = "admin:adminpass",
    org= "myorg"
)

write_api = client.write_api()

def save_to_postgres(record):
    PG_CUR.execute("INSERT INTO flights VALUES (%s,%s,%s,%s,%s,%s)",
                record["icao24"],record["callsign"], record["lat"],
                record["lon"], record["velocity"], record["timestamp"])
    PG_CONN.commit()

def save_to_influx(record):
    p = Point("flights")\
        .tag("icao24",record["icao24"])\
        .field("lat", record["lat"])\
        .field("lon", record["lon"])\
        .field("velocity", record["velocity"])\
        .time(record["timestamp"], WritePrecision.S)
    write_api.write(bucket="telemetry", record=p)