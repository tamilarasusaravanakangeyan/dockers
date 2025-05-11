### To create Topic

```

docker exec -it bb1385096234 /opt/kafka/bin/kafka-topics.sh --create --topic new_topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

### To list topics

```
docker exec -it bb1385096234 /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
```

### To send message to topic

```
docker exec -it bb1385096234 /bin/bash
```

```
/opt/kafka/bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic my_topic
```

### To read message from topic

```
docker exec -it bb1385096234 /bin/bash
```

```
/opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic my_topic --from-beginning
```
