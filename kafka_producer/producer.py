#!/usr/bin/env python3

import csv
import time
import random
from kafka.producer import KafkaProducer
import json
import datetime

producer = KafkaProducer(bootstrap_servers='10.105.88.58:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))


while True:
    try:
        for pos in range(1, 101, 3):
            msg = {"timestamp" : str(datetime.datetime.now())[:19], "carid":1, "position": pos, "speed":random.randint(45, 82)}
            producer.send('input', msg)
            time.sleep(1.5)

        for pos in range(1, 101, 3):
            msg = {"timestamp" : str(datetime.datetime.now())[:19], "carid":2, "position": pos, "speed":random.randint(45, 82)}
            producer.send('input', msg)
            time.sleep(2)

        for pos in range(1, 101, 3):
            msg = {"timestamp" : str(datetime.datetime.now())[:19], "carid":3, "position": pos, "speed":random.randint(45, 82)}
            producer.send('input', msg)
            time.sleep(2.5)
    except:
        pass