#!/usr/bin/env python3

import os, time, json

try:
    # Docker Hub Credentials
    docker_username = "change_username"
    docker_password = "change_password"
    
    # Deleting earlier deployments before creation
    os.system("kubectl delete -n default deployment hive-mqtt-broker")
    os.system("kubectl delete -n default service hive-mqtt-broker")
    os.system("kubectl delete -n default deployment hive-mqtt-publisher")
    os.system("kubectl delete -n default deployment hive-mqtt-subscriber")
    os.system("kubectl delete -n default deployment kafka-zookeeper-consumer")
    os.system("kubectl delete -n default deployment kafka-zookeeper-producer")
    os.system("kubectl delete -n default deployment kafka-zookeeper-broker")
    os.system("kubectl delete -n default service kafka-zookeeper-broker")
    os.system("kubectl delete -n default service kafka-spark")
    time.sleep(10)
    os.system("minikube image rm docker.io/"+docker_username+"/sp23:hive-mqtt-broker")
    os.system("minikube image rm docker.io/"+docker_username+"/sp23:hive-mqtt-publisher")
    os.system("minikube image rm docker.io/"+docker_username+"/sp23:hive-mqtt-subscriber")
    os.system("minikube image rm docker.io/"+docker_username+"/sp23:kafka-zookeeper-consumer")
    os.system("minikube image rm docker.io/"+docker_username+"/sp23:kafka-zookeeper-producer")
    os.system("minikube image rm docker.io/"+docker_username+"/sp23:kafka-zookeeper-broker")
    os.system("minikube image rm docker.io/"+docker_username+"/sp23:kafka-spark")
    time.sleep(10)
    os.system("docker image rm -f "+docker_username+"/sp23:hive-mqtt-publisher")
    os.system("docker image rm -f "+docker_username+"/sp23:hive-mqtt-subscriber")
    os.system("docker image rm -f "+docker_username+"/sp23:kafka-zookeeper-consumer")
    os.system("docker image rm -f "+docker_username+"/sp23:kafka-zookeeper-producer")
    os.system("docker image rm -f "+docker_username+"/sp23:kafka-zookeeper-broker")
    os.system("docker image rm -f "+docker_username+"/sp23:kafka-spark")
    os.system("docker image rm -f hive-mqtt-subscriber:latest")
    os.system("docker image rm -f hive-mqtt-publisher:latest")
    os.system("docker image rm -f kafka-zookeeper-consumer:latest")
    os.system("docker image rm -f kafka-zookeeper-producer:latest")
    os.system("docker image rm -f kafka-zookeeper-producer")
    os.system("docker image rm -f kafka-zookeeper-broker:latest")
    os.system("docker image rm -f kafka-spark:latest")
    time.sleep(10)

    print("[+] Deleted previous deployments and old images from Kubernetes and Minikube\n")
    time.sleep(20)
    # Docker Hub login for pushing images
    os.system("docker login -u "+docker_username+ " -p "+docker_password+ " docker.io")
    print("[+] Successfully logged in into DockerHub using the profile installed on the machine\n")

    # HiveMQ MQTT Broker Setup 
    print("[+] Creation of Hive MQTT Broker initiated")
    os.system("kubectl create deployment hive-mqtt-broker --image=hivemq/hivemq4")
    time.sleep(20)
    os.system("kubectl expose deployment hive-mqtt-broker --type=LoadBalancer --port 1883")
    print("[+] Successfully initiated the creation of Broker Pod and Service expose on Kubernetes \n")
    time.sleep(20) # Giving some time for container to spawn up

    # Getting Broker's Service IP info
    os.system("kubectl get service hive-mqtt-broker -o json > Service_IP.json")
    filename = "Service_IP.json"
    broker_service_info = json.load(open(str(filename), 'r'))
    #new_broker_ip = broker_service_info["status"]["loadBalancer"]["ingress"][0]["ip"]
    new_broker_ip = broker_service_info["spec"]["clusterIPs"][0]
    print(new_broker_ip)
    print("[+] Successfully got the updated IP")
    time.sleep(20)

    # Navigating to MQTT Subscriber folder
    print("[+] Python subscriber setup")
    current_dir = os.getcwd()
    new_dir = current_dir + "/python3_sub"
    os.chdir(new_dir)

    # Change the IP info on sub.py 
    with open('sub.py', 'r', encoding='utf-8') as file:
        data = file.readlines()
    data[14] = "client.connect('"+new_broker_ip+"', 1883)\n"
    with open('sub.py', 'w', encoding='utf-8') as file1:
        file1.writelines(data)

    # MQTT Subscriber Setup
    print("[+] Initiated docker build for subscriber \n")
    os.system("docker build -t hive-mqtt-subscriber -f Dockerfile . --no-cache")
    print("[+] docker subscriber built successfully\n")
    os.system("docker tag hive-mqtt-subscriber:latest "+docker_username+"/sp23:hive-mqtt-subscriber")
    os.system("docker push "+docker_username+"/sp23:hive-mqtt-subscriber")
    os.system("kubectl create deployment hive-mqtt-subscriber --image="+docker_username+"/sp23:hive-mqtt-subscriber")
    print("[+] Successfully created Subscriber on Kubernetes \n")
    time.sleep(10) # Giving some time for container to spawn up

    # Navigating to MQTT Publisher folder 
    print("[+] Python publisher setup")
    os.chdir("../")
    current_dir = os.getcwd()
    new_dir = current_dir + "/python3_pub"
    os.chdir(new_dir)
    print("[+] Successfully navigated to pub folder")

    # Change the IP info on pub.py 
    with open('pub.py', 'r', encoding='utf-8') as file:
        data = file.readlines()
    print(data[13])
    data[13] = "client.connect('"+new_broker_ip+"', 1883)\n"
    with open('pub.py', 'w', encoding='utf-8') as file:
        file.writelines(data)
    print("[+] Successfully got the updated IP")
    # MQTT Publisher Setup
    print("[+] Initiated docker build for publisher \n")
    os.system("docker build -t hive-mqtt-publisher -f Dockerfile . --no-cache")
    print("[+] docker publisher built successfully\n")
    os.system("docker tag hive-mqtt-publisher:latest "+docker_username+"/sp23:hive-mqtt-publisher")
    os.system("docker push "+docker_username+"/sp23:hive-mqtt-publisher")
    os.system("kubectl create deployment hive-mqtt-publisher --image="+docker_username+"/sp23:hive-mqtt-publisher")
    print("[+] Successfully created Publisher on Kubernetes \n")
    os.chdir("../")
    time.sleep(10) # Giving some time for container to spawn up
    
    # Navigating to Kafka Broker folder 
    print("[+] Kafka Broker setup")
    current_dir = os.getcwd()
    new_dir = current_dir + "/kafka_broker"
    os.chdir(new_dir)
    print("[+] Successfully navigated to kafka_consumer folder")

    # Kafka Setup
    print("[+] Creation of Kafka Broker initiated")
    os.system("docker build -t kafka-zookeeper-broker -f Dockerfile . --no-cache")
    print("[+] docker kafka-zookeeper-consumer built successfully\n")
    os.system("docker tag kafka-zookeeper-broker:latest "+docker_username+"/sp23:kafka-zookeeper-broker")
    os.system("docker push "+docker_username+"/sp23:kafka-zookeeper-broker")
    os.system("kubectl create deployment kafka-zookeeper-broker --image="+docker_username+"/sp23:kafka-zookeeper-broker")
    
    # os.system("kubectl create deployment kafka-zookeeper-broker --image=johnnypark/kafka-zookeeper")
    time.sleep(20)
    os.system("kubectl expose deployment kafka-zookeeper-broker --type=LoadBalancer --port 9092")
    print("[+] Successfully initiated the creation of Kafka Broker Pod and Service expose on Kubernetes \n")
    time.sleep(20) # Giving some time for container to spawn up

    # Update IP of Kafka Broker on Consumers
    print("[+] Looking for Kafka Broker IP \n")
    os.system("kubectl get service kafka-zookeeper-broker -o json > Service_IP_Kafka.json")
    filename = "Service_IP_Kafka.json"
    kafka_broker_service_info = json.load(open(str(filename), 'r'))
    #new_broker_ip = broker_service_info["status"]["loadBalancer"]["ingress"][0]["ip"]
    kafka_new_broker_ip = kafka_broker_service_info["spec"]["clusterIPs"][0]
    print("[+] Updated IP: "+ str(kafka_new_broker_ip))
    os.chdir("../")
    time.sleep(2)

    # Navigating to Kafka Consumer folder 
    print("[+] Kafka Consumer setup")
    current_dir = os.getcwd()
    new_dir = current_dir + "/kafka_consumer"
    os.chdir(new_dir)
    print("[+] Successfully navigated to kafka_consumer folder")

    # Updating the IP on Kafka consumer.py file
    with open('consumer.py', 'r', encoding='utf-8') as file2:
        data1 = file2.readlines()
    print(data1[13])
    data1[6] = "producer = KafkaProducer(bootstrap_servers='"+kafka_new_broker_ip+":9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))\n"
    data1[7] = "consumer = KafkaConsumer(bootstrap_servers='"+kafka_new_broker_ip+":9092', value_deserializer = lambda x : json.loads(x.decode('utf-8')))\n"
    with open('consumer.py', 'w', encoding='utf-8') as file2:
        file2.writelines(data1)
    print("[+] Successfully updated the IP on consumer.py")

    # Kafka Consumer Setup
    print("[+] Initiated docker build for kafka consumer \n")
    os.system("docker build -t kafka-zookeeper-consumer -f Dockerfile . --no-cache")
    print("[+] docker kafka-zookeeper-consumer built successfully\n")
    os.system("docker tag kafka-zookeeper-consumer:latest "+docker_username+"/sp23:kafka-zookeeper-consumer")
    os.system("docker push "+docker_username+"/sp23:kafka-zookeeper-consumer")
    os.system("kubectl create deployment kafka-zookeeper-consumer --image="+docker_username+"/sp23:kafka-zookeeper-consumer")
    print("[+] Successfully created Kafka Consumer on Kubernetes \n")
    os.chdir("../")
    time.sleep(10) # Giving some time for container to spawn up

   # Navigating to Kafka Producer folder 
    print("[+] Kafka Producer setup")
    current_dir = os.getcwd()
    new_dir = current_dir + "/kafka_producer"
    os.chdir(new_dir)
    print("[+] Successfully navigated to kafka_producer folder")

    # Update IP of Kafka Broker on Producer
    print("[+] Looking for Kafka Broker IP \n")
    os.system("kubectl get service kafka-zookeeper-broker -o json > Service_IP_Kafka.json")
    filename = "Service_IP_Kafka.json"
    kafka_broker_service_info = json.load(open(str(filename), 'r'))
    #new_broker_ip = broker_service_info["status"]["loadBalancer"]["ingress"][0]["ip"]
    kafka_new_broker_ip = kafka_broker_service_info["spec"]["clusterIPs"][0]
    print("[+] Updated IP: "+ str(kafka_new_broker_ip))
    time.sleep(2)

    # Updating the IP on Kafka producer.py file
    with open('producer.py', 'r', encoding='utf-8') as file2:
        data1 = file2.readlines()
    data1[9] = "producer = KafkaProducer(bootstrap_servers='"+kafka_new_broker_ip+":9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))\n"
    with open('producer.py', 'w', encoding='utf-8') as file2:
        file2.writelines(data1)
    print("[+] Updated IP on producer.py: "+ str(kafka_new_broker_ip))

    # Kafka Producer Setup
    print("[+] Initiated docker build for kafka producer \n")
    os.system("docker build -t kafka-zookeeper-producer -f Dockerfile . --no-cache")
    print("[+] docker kafka-zookeeper-producer built successfully\n")
    os.system("docker tag kafka-zookeeper-producer:latest "+docker_username+"/sp23:kafka-zookeeper-producer")
    os.system("docker push "+docker_username+"/sp23:kafka-zookeeper-producer")
    os.system("kubectl create deployment kafka-zookeeper-producer --image="+docker_username+"/sp23:kafka-zookeeper-producer")
    print("[+] Successfully created Kafka Producer on Kubernetes \n")
    os.chdir("../")
    time.sleep(10) # Giving some time for container to spawn up

    # # Update IP of Kafka Broker on Producer
    # print("[+] Looking for Kafka Broker IP \n")
    # os.system("kubectl get service kafka-zookeeper-broker -o json > Service_IP_Kafka.json")
    # filename = "Service_IP_Kafka.json"
    # kafka_broker_service_info = json.load(open(str(filename), 'r'))
    # #new_broker_ip = broker_service_info["status"]["loadBalancer"]["ingress"][0]["ip"]
    # kafka_new_broker_ip = kafka_broker_service_info["spec"]["clusterIPs"][0]
    # print("[+] Updated IP: "+ str(kafka_new_broker_ip))
    # time.sleep(2)

    # # Updating the IP on Kafka producer.py file
    # with open('spark_job.py', 'r', encoding='utf-8') as file2:
    #     data1 = file2.readlines()
    # data1[11] = "        .option('kafka.bootstrap.servers', '"+kafka_new_broker_ip+":9092') \ \n"
    # data1[31] = "        .option('kafka.bootstrap.servers', '"+kafka_new_broker_ip+":9092') \ \n"
    # with open('spark_job.py', 'w', encoding='utf-8') as file2:
    #     file2.writelines(data1)
    # print("[+] Updated IP on spark_job.py: "+ str(kafka_new_broker_ip))

    # # Installing Apache Spark Setup
    # print("[+] Creation of Spark Job initiated")
    # os.system("kubectl create deployment kafka-spark --image=apache/spark")
    # time.sleep(20)
    # print("[+] Successfully initiated the creation of Apache Spark Pod on Kubernetes \n")
    # #time.sleep(20) # Giving some time for container to spawn up

except Exception as e:
    print("[-] Error: "+str(e))
    pass