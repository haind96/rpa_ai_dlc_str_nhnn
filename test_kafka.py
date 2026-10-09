import uuid
from confluent_kafka import Consumer

def test_consumer():
    bootstrap = "192.168.0.2:9093"
    username = "admin"
    password = "admin123"
    topic = "RPA_STR_NHNN_INPUT"

    print("Starting test consumer...")
    conf = {
        'bootstrap.servers': bootstrap,
        'group.id': 'TEST_GROUP_MANUAL',
        'auto.offset.reset': 'earliest',
        'security.protocol': 'SASL_PLAINTEXT',
        'sasl.mechanism': 'PLAIN',
        'sasl.username': username,
        'sasl.password': password,
        'debug': 'cgrp,fetch'
    }
    
    c = Consumer(conf)
    
    from confluent_kafka import TopicPartition, OFFSET_BEGINNING
    
    # Bypass consumer group by manually assigning the partition and offset
    c.assign([TopicPartition(topic, 0, OFFSET_BEGINNING)])
    print("Manually assigned to partition 0 with OFFSET_BEGINNING")
    
    print("Polling...")
    try:
        while True:
            msg = c.poll(1.0)
            if msg is None:
                pass # print("No message")
            elif msg.error():
                print(f"Error: {msg.error()}")
            else:
                print(f"Received: {msg.value().decode('utf-8')}")
    except KeyboardInterrupt:
        pass
        
    c.close()

if __name__ == "__main__":
    test_consumer()
