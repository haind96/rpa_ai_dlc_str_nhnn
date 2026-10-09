import json
from typing import Callable, Dict, Any, Generator
from contextlib import contextmanager

from confluent_kafka import Consumer, KafkaError, TopicPartition, OFFSET_BEGINNING
from loguru import logger

from src.config import AppConfig


@contextmanager
def get_kafka_consumer(config: AppConfig) -> Generator[Consumer, None, None]:
    """Create and configure a Kafka consumer as a context manager to ensure safe teardown."""
    conf = {
        'bootstrap.servers': config.kafka_bootstrap_servers,
        # group.id is required by librdkafka even if we manually assign, 
        # but we set enable.auto.commit to False to avoid coordinator errors.
        'group.id': config.kafka_group_id,
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False,
        'security.protocol': 'SASL_PLAINTEXT',
        'sasl.mechanism': 'PLAIN',
        'sasl.username': config.kafka_username,
        'sasl.password': config.kafka_password,
        'error_cb': lambda err: logger.error(f"Kafka error callback: {err}"),
    }
    
    consumer = Consumer(conf)
    try:
        yield consumer
    finally:
        # Guarantee the connection is closed when exiting the context block
        consumer.close()
        logger.info("Kafka consumer connection explicitly closed.")


def consume_messages(config: AppConfig, process_message: Callable[[Dict[str, Any]], bool]) -> None:
    """Consume messages from Kafka and process them using the provided callback."""
    
    with get_kafka_consumer(config) as consumer:
        # Bypass consumer group coordinator by manually assigning the partition
        # and forcing it to read from the beginning.
        partition = TopicPartition(config.kafka_topic, 0, OFFSET_BEGINNING)
        consumer.assign([partition])

        logger.info(f"Started manually consuming from topic {config.kafka_topic} (partition 0, OFFSET_BEGINNING)")
        
        try:
            while True:
                msg = consumer.poll(timeout=1.0)
                
                if msg is None:
                    continue
                    
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event, not an error
                        continue
                    else:
                        logger.error(f"Kafka error: {msg.error()}")
                        break

                try:
                    # Decode the message
                    value = msg.value().decode('utf-8')
                    logger.info(f"Received raw message from Kafka: {value}")
                    data = json.loads(value)
                    
                    if process_message(data):
                        logger.info("Message processed successfully. Terminating consumer loop as requested.")
                        break
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to decode message as JSON: {e}. Raw msg: {msg.value()}")
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    
        except KeyboardInterrupt:
            logger.info("Aborted by user.")
