from kafka import KafkaConsumer
from influxdb import InfluxDBClient
import json

# Kafka Consumer
consumer = KafkaConsumer(
    "sensor_data",
    bootstrap_servers="kafka:9092",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

# InfluxDB Client
influx_client = InfluxDBClient(host="influxdb", port=8086, database="kafkadb")

for message in consumer:
    data = message.value
    json_body = [
        {
            "measurement": "sensor_data",
            "tags": {
                "sensor_id": data["sensor_id"]
            },
            "fields": {
                "temperature": data["temperature"]
            },
            "time": data["timestamp"]
        }
    ]
    influx_client.write_points(json_body)
    print(f"Saved to InfluxDB: {data}")
