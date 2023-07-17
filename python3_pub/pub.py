import paho.mqtt.client as paho
import time
import json
import datetime
import os
import sys

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))
 
client = paho.Client()
client.on_publish = on_publish
#Change the IP address to Service's IP mentioned in Minikube dashboard -> Service
# client.connect(<Service_IP>, 1883)
client.connect('10.97.155.110', 1883)

client.loop_start()

filename = 'infra_update.json'

#########################
# CHANGES HERE
########################

def json_object_creator():
    return {
        "pods": [],
        "services": [],
        "deployments": [],
        "replicaSets": []
    }

def empty_sample_dict():
    return dict({
        "timestamp": [],
        "kind": [],
        "podIP": [],
        "clusterIP": [],
        "object_name": [],
        "application": [],
        "Available_replicaSets": [],
        "Current_replicaSets": []
    })

try:
    #os.remove('edgetcd.json')
    os.remove('objects.json')
except:
    pass

filen = f"edgetcd.json"
important = {}
try:
    while True:
        time.sleep(10) # latency = 10 lazy synch for important metadata
        
        # Initialization
        timedate = str(datetime.datetime.now()).split(" ")[0]
        data = json.load(open(str(filename), 'r')) # Transfer to live reading eventually
        
        for i in data['items']:
            areplica = 'None'
            rreplica = 'None'
            ip = 'None'
            podip = 'None'
            app = 'None'
            if i['kind'] == "Service":  
                timestamp = str(datetime.datetime.now()).split(" ")[1]
                if 'selector' in i['spec']:
                    kind = i['kind']
                    ip = i['spec']['clusterIP']
                    name = i['metadata']['name']
                    #app = i['spec']['selector']['app']
                else:  
                    kind = i['kind']
                    ip = i['spec']['clusterIP']
                    name = i['metadata']['name']
                    app = 'None'
                (rc, mid) = client.publish('time', str(timestamp), qos=1)
                (rc, mid) = client.publish('time/kind', str(kind), qos=1)
                (rc, mid) = client.publish('time/kind/clusterIP', str(ip), qos=1)
                (rc, mid) = client.publish('time/kind/clusterIP/name', str(name), qos=1)
                (rc, mid) = client.publish('time/kind/clusterIP/name/app', str(app), qos=1)
                important[timestamp] = empty_sample_dict()
                important[timestamp]['timestamp'] = timestamp
                important[timestamp]['kind'] = str(kind)
                important[timestamp]['clusterIP'] = str(ip)
                important[timestamp]['podIP'] = str(podip)
                important[timestamp]['object_name'] = str(name)
                important[timestamp]['application'] = str(app)
                important[timestamp]['Available_replicaSets'] = str(areplica)
                important[timestamp]['Current_replicaSets'] = str(rreplica)
            if i['kind'] == "Pod": 
                timestamp = str(datetime.datetime.now()).split(" ")[1] 
                kind = i['kind']
                podip = i['status']['podIP']
                name = i['metadata']['name']
                #app = i['metadata']['labels']['app']
                (rc, mid) = client.publish('time', str(timestamp), qos=1)
                (rc, mid) = client.publish('time/kind', str(kind), qos=1)
                (rc, mid) = client.publish('time/kind/podIP', str(podip), qos=1)
                (rc, mid) = client.publish('time/kind/podIP/name', str(name), qos=1)
                (rc, mid) = client.publish('time/kind/podIP/name/app', str(app), qos=1)
                important[timestamp] = empty_sample_dict()
                important[timestamp]['timestamp'] = timestamp
                important[timestamp]['kind'] = str(kind)
                important[timestamp]['clusterIP'] = str(ip)
                important[timestamp]['podIP'] = str(podip)
                important[timestamp]['object_name'] = str(name)
                important[timestamp]['application'] = str(app)
                important[timestamp]['Available_replicaSets'] = str(areplica)
                important[timestamp]['Current_replicaSets'] = str(rreplica)
            if i['kind'] == "Deployment": 
                timestamp = str(datetime.datetime.now()).split(" ")[1] 
                kind = i['kind']
                name = i['metadata']['name']
                #app = i['metadata']['labels']['app']
                #areplica = i['status']['availableReplicas']
                rreplica = i['status']['replicas']
                (rc, mid) = client.publish('time', str(timestamp), qos=1)
                (rc, mid) = client.publish('time/kind', str(kind), qos=1)
                (rc, mid) = client.publish('time/kind/name', str(name), qos=1)
                (rc, mid) = client.publish('time/kind/name/app', str(app), qos=1)
                (rc, mid) = client.publish('time/kind/name/app/availableReplicas', str(areplica), qos=1)
                (rc, mid) = client.publish('time/kind/name/app/replicas', str(rreplica), qos=1)
                important[timestamp] = empty_sample_dict()
                important[timestamp]['timestamp'] = timestamp
                important[timestamp]['kind'] = str(kind)
                important[timestamp]['clusterIP'] = str(ip)
                important[timestamp]['podIP'] = str(podip)
                important[timestamp]['object_name'] = str(name)
                important[timestamp]['application'] = str(app)
                important[timestamp]['Available_replicaSets'] = str(areplica)
                important[timestamp]['Current_replicaSets'] = str(rreplica)
            if i['kind'] == "ReplicaSet":
                timestamp = str(datetime.datetime.now()).split(" ")[1] 
                kind = i['kind']
                name = i['metadata']['name']
                #app = i['metadata']['labels']['app']
                #areplica = i['status']['availableReplicas']
                rreplica = i['status']['replicas']
                (rc, mid) = client.publish('time', str(timestamp), qos=1)
                (rc, mid) = client.publish('time/kind', str(kind), qos=1)
                (rc, mid) = client.publish('time/kind/name', str(name), qos=1)
                (rc, mid) = client.publish('time/kind/name/app', str(app), qos=1)
                (rc, mid) = client.publish('time/kind/name/app/availableReplicas', str(areplica), qos=1)
                (rc, mid) = client.publish('time/kind/name/app/replicas', str(rreplica), qos=1)
                important[timestamp] = empty_sample_dict()
                important[timestamp]['timestamp'] = timestamp
                important[timestamp]['kind'] = str(kind)
                important[timestamp]['clusterIP'] = str(ip)
                important[timestamp]['podIP'] = str(podip)
                important[timestamp]['object_name'] = str(name)
                important[timestamp]['application'] = str(app)
                important[timestamp]['Available_replicaSets'] = str(areplica)
                important[timestamp]['Current_replicaSets'] = str(rreplica)
                
except KeyboardInterrupt:
    for i in important:
        if important[i]['podIP'] == 'None':
            important[i].pop('podIP')
        if important[i]['clusterIP'] == 'None':
            important[i].pop('clusterIP')
        if important[i]['application'] == 'None':
            important[i].pop('application')
        if important[i]['Available_replicaSets'] == 'None':
            important[i].pop('Available_replicaSets')
        if important[i]['Current_replicaSets'] == 'None':
            important[i].pop('Current_replicaSets')
    with open(filen, 'w') as fout:
        json_dumps_str = json.dumps(important, indent=4)
        print(json_dumps_str, file=fout)

    struct = {}
    newfile = 'objects.json'
    struct = json_object_creator()
    new = json.load(open(str(filen), 'r'))
    for i in new:
        if new[i]['kind'] == 'Pod':
            struct['pods'].append(new[i])
        if new[i]['kind'] == 'Service':
            struct['services'].append(new[i])
        if new[i]['kind'] == 'Deployment':
            struct['deployments'].append(new[i])
        if new[i]['kind'] == 'ReplicaSet':
            struct['replicaSets'].append(new[i])
    with open(newfile, 'w') as fn:
        json_check = json.dumps(struct, indent=4)
        print(json_check, file=fn)

    os.remove('edgetcd.json')
    sys.exit(0) 
