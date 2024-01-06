from confluent_kafka import Consumer, KafkaError

consumer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'your_consumer_group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_conf)

topic = 'login_events_topic'
consumer.subscribe([topic])

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break

        print(f'Received message: {msg.value().decode("utf-8")}')

except KeyboardInterrupt:
    pass

finally:
    consumer.close()
