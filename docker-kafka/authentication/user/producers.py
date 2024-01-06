from confluent_kafka import Producer, KafkaException
from confluent_kafka.admin import NewTopic , AdminClient

def create_topic(admin_conf, topic_name):
    admin_client = AdminClient(admin_conf)
    existing_topics = admin_client.list_topics(timeout=5).topics
    if topic_name not in existing_topics:
        new_topic = NewTopic(topic=topic_name, num_partitions=1, replication_factor=1)
        try:
            admin_client.create_topics([new_topic])
        except KafkaException as e:
            print(f"Failed to create topic: {e}")
        finally:
            admin_client.close()

admin_conf = {'bootstrap.servers': 'localhost:9092'}
topic_name = 'login_events_topic'

create_topic(admin_conf, topic_name)

# Create a producer
producer_conf = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(producer_conf)

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')

def send_login_event(username):
    # Simulating a successful login event
    message_value = f'Successful login for user: {username}'
    producer.produce(topic=topic_name, value=message_value, callback=delivery_report)

# Example: Sending a login event for user 'john_doe'
send_login_event('john_doe')

# Flush the producer to ensure all messages are delivered before exiting
producer.flush()

# Note: 'producer.close()' is not needed in the latest confluent_kafka versions

print("Producer script completed.")
