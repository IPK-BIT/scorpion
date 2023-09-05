from icecream import ic
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("INFLUXDB_TOKEN")
org = "scorpion"
url = "http://influxdb:8086"
bucket="kpis"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()
delete_api = client.delete_api()