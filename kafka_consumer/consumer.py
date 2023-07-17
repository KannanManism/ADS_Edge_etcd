#!/usr/bin/env python
import json 
# from kafka import KafkaProducer, KafkaConsumer
from kafka.consumer import KafkaConsumer
from kafka.producer import KafkaProducer

producer = KafkaProducer(bootstrap_servers='10.105.88.58:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
consumer = KafkaConsumer(bootstrap_servers='10.105.88.58:9092', value_deserializer = lambda x : json.loads(x.decode('utf-8')))

consumer.subscribe("input")
for msg in consumer:
    message = msg.value
    position = message['position']

    if position > 0 and position <= 35:
        message['tower'] = 1
#         producer.send("bloomington_tower", message)
    elif position > 35 and position <= 70:
        message['tower'] = 2
#         producer.send("moorseville_tower", message)
    else:
        message['tower'] = 3
    producer.send("towers", message)