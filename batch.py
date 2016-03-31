from kafka import KafkaConsumer
import json
import time

print("HEY MAN!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
time.sleep(10)

consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])

# while True:
# 	for message in consumer:
# 		new_listing = json.loads((message.value).decode('utf-8'))
# 		print(new_listing)
