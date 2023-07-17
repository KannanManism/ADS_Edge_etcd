import paho.mqtt.client as paho

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))
 
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))    

client = paho.Client()
client.on_subscribe = on_subscribe
client.on_message = on_message

#Change the IP address to Service's IP mentioned in Minikube dashboard -> Service
# client.connect(<Service_IP>, 1883)
client.connect('10.110.97.168', 1883)

# ****************************************
# Make your code changes after this line
# ****************************************

#client.subscribe('speed/#', qos=1)
client.subscribe('time/#', qos=1)

client.loop_forever()