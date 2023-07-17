# syntax=docker/dockerfile:1

FROM johnnypark/kafka-zookeeper
WORKDIR /kafka_broker
# RUN /bin/bash -c '/opt/kafka_2.13-2.6.0/bin/kafka-console-consumer.sh --bootstrap-server 10.98.76.58:9092 --topic towers'
# RUN /bin/bash -c '/opt/kafka_2.13-2.6.0/bin/kafka-console-consumer.sh --bootstrap-server 10.98.76.58:9092 --topic input'
# RUN /bin/bash -c '/opt/kafka_2.13-2.6.0/bin/kafka-console-consumer.sh --bootstrap-server 10.98.76.58:9092 --topic output'

SHELL ["/bin/bash", "-c", "/opt/kafka_2.13-2.6.0/bin/kafka-topics.sh", "--create", "--topic", "output", "--bootstrap-server", "localhost:9092"] \
& ["/bin/bash", "-c", "/opt/kafka_2.13-2.6.0/bin/kafka-topics.sh", "--create", "--topic", "towers", "--bootstrap-server", "localhost:9092"] \
& ["/bin/bash", "-c", "/opt/kafka_2.13-2.6.0/bin/kafka-topics.sh", "--create", "--topic", "input", "--bootstrap-server", "localhost:9092"] \
& ["/bin/bash", "-c", "/opt/kafka_2.13-2.6.0/bin/kafka-console-consumer.sh", "--bootstrap-server", "localhost:9092", "--topic", "input"] \
& ["/bin/bash", "-c", "/opt/kafka_2.13-2.6.0/bin/kafka-console-consumer.sh", "--bootstrap-server", "localhost:9092", "--topic", "output"] \
& ["/bin/bash", "-c", "/opt/kafka_2.13-2.6.0/bin/kafka-console-consumer.sh", "--bootstrap-server", "localhost:9092", "--topic", "towers"]