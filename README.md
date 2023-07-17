# CSCI-B649 Course Project Report: Achieving High Availability with Eventual Consistency on Edge Etcds

## For the successful deployment in Kubernetes 
- Open the `automation.py` and edit line 7 and 8 with Docker Hub `username` and `password` for automated execution
    * *Note: This script deletes previous cache and builds on Kubernetes and local machine*
    * *Note: automation.py takes care of IP configurations, deployment, and script executions inside the pod*
### Run the automation.py file using the command
- *python3 automation.py*

### Tested Environment: Ubuntu 20.04.1

# Archive
## Sign in into Docker
*docker login -u "<docker_username>" -p "<docker_password>" docker.io* 

## Hivemq Broker creation

*kubectl create deployment hive-mqtt-broker --image=hivemq/hivemq4*

*kubectl expose deployment hive-mqtt-broker --type=LoadBalancer --port=1883*


## Hivemq Publisher
### Navigate to the python3_pub file and run the cmds

#### Note: Go to Minikube Dashboard -> Service. Check the IP address of the Broker
#### Update this IP address on pub.py and sub.py in the respective folders
#### Later, navigate to the respective folder and run the following command
*docker build -t hive-mqtt-publisher -f Dockerfile . --no-cache*

*docker tag hive-mqtt-publisher:latest <dockerhub_username>/sp23:hive-mqtt-publisher*

*docker push <dockerhub_username>/sp23:hive-mqtt-publisher*

## publisher deployment to kubernetes
*kubectl create deployment hive-mqtt-publisher --image=<dockerhub_username>/sp23:hive-mqtt-publisher*

## Hivemq Subscriber
### Navigate to the python3_sub file and run the cmds

*docker build -t hive-mqtt-subscriber -f Dockerfile . --no-cache*

*docker tag hive-mqtt-subscriber:latest <dockerhub_username>/sp23:hive-mqtt-subscriber*

*docker push <dockerhub_username>/sp23:hive-mqtt-subscriber*

## subscriber deployment to kubernetes
*kubectl create deployment hive-mqtt-subscriber --image=<dockerhub_username>/sp23:hive-mqtt-subscriber*
