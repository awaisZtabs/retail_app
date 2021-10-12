
from json import dumps
from time import sleep

from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x:
                         dumps(x).encode('utf-8'))

data = {"messageid": "e17c138f-0e46-4a64-ae58-1ea88f4a5441",
        "mdsversion": "1.0",
        'camera_id': '1',
        "@timestamp": "2021-09-21T05:12:51.014Z",
        "analyticsModule": {
            "Frame_ID": 4610.0,
            "occupancy": 23.0,
            "Entry": 25.0,
            "Exit": 2.0,
            "Tracking-ID": 394.0,
            "X_Coordinate": 847.0,
            "Y_Coordinate": 222.0
        },
        "event": {
            "id": "ASIFsBC"
        }}
producer.send('numtesst', value=data)
sleep(5)
