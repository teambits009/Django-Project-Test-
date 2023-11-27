# Django-Project-Test-

SECTION A 

QUESTION 1: 
Give examples of different integration protocols you have come across and give example scripts in python3 on how to achieve each one (10points)

- Integration protocols are communication standards that allow different software systems to exchange information. There are several integration protocols commonly used in software development. 

1. REST APIS ( Representational State Transfer):
REST is an architectural style that uses the standard HTTP methods (GET, POST, PUT,DELETE) for communication. It is widely used for web services. 

Scripts using 'request' library:

import requests 
#Get request 
response = requests.get ("https://jsonplaceholder.typicode.com/todos/1")
print(response.json())

#POST request 
new_todo = {"title": "Buy groceries", "completed": False}
response  = request.post ("https://jsonplaceholder.typicode.com/todos", json=new_todo)
print(response.json())


2. SOAP (Simple Object Access Protocol):
SOAP is a protocol for exchanging structured information in web services. It uses XML  for message format and can be transported over HTTP, SMPTP, etc 

Example Script using 'zeep' library:

from zeep import Client
#Create a SOAP client 
client = Client('https://www.example.com/soap-endpoint?wsdI')
#Call a SOAP operation 
result = client.service.SomeOperation( parameter1='value', parameter2='value2')
print(result)


3. GraphQL:
GraphQL is a query language for APIs and runtime for excuting those queries. It allows clients to request only the data they need. 

Scripts using 'request' library: 
import requests 

url = 'https://api.example.com/graphql'
query= '''
  query {
    user(id: 1) {
          name 
          email
    }
  }
'''

response = requests.post(url, json= {'query': query})
print(response.json())

4. MQTT (Message Queuing Telemetrty Transport): 
MQTT is a lightweight and efficient messaging protocol, often used in IoT applications. 

Scripts using 'paho-mqtt' library: 
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Connected with results code {rc}")
    client.subscribe("topic")

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")

client = mqtt.client()
client.on_connect=on_connect
client.on_message=on_message

client.connect("mqtt.eclipse.org", 1883, 60)
client.loop_forever()


5. WebSockets: 
WebSockets provide a full-deplex communication channel over a single, long-lived connection. They are suitable for real-time applications. 

Script using 'websockets' library: 

import asyncio
import websockets

async def echo (websocket, path)
      async for message in websocket: 
          await websocket.send(message)

start_server= websockets.server(echo, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

N/B: You may need to install additional libraries before running these scripts using pip install ('requests','zeep','paho-mqtt', 'websockets'). 
The URLs and endpoints used in these examples are placeholders thus should be replaced with actual values from the integration scenario. 


...............................................................................................................


QUESTION 2: 
 Give a walkthrough of how you will manage a data streaming application sending one million notifications every hour while giving examples of technologies and configurations you will use to manage load and asynchronous services. (10Points)

 - A data streaming application that sends one million notifications every hour requires careful consideration of scalability, reliability,and efficiency. 
Lets work this out in a logical design pattern using these configurations and technologies.

1. Message Broker:
Lets use a message broker to handle the communication between different components of your application. A popular choice is Apache Kafka

Installation: 
#Install Kafka 
#Example for macOS using Homebrew 
brew install kafka 

Configuration: 
Adjust Kafka configuration files('server.properties')to accommodate high throughput. 

2. Notification Service: 
Create a dedicated service to handle notifications asychronously. This service can subscribe to the Kafka topic where notifications are produced. 

An Example using Python with 'confluent_kafka' library:
from confluent_kafka import Consumer, KafkaError

consumer_conf = {
    'bootstrap.services': 'kafka-broker_address',
    'group.id: 'notification-group', 
    'auto.offset.rest': 'earliest'
}

consumer = Consumer(consumer_conf)
consumer.subsribe(['notification_topic'])

while True:
    msg = consumer.poll(1.0)
     if msg is None:
        continue 
    if msg.error():
       if msg.error().code() == KafkaError._PARTITION_EOF: 
          continue 
       else: 
           print(msg.error())
           break 
      #Process the Notification asynchronously 
      process_notification(msg.value())


3. Asynchronous Processing:
To handle the scale of one million notifications, it's crucial to process them asynchronous. Celery is a popular choice for this. 

Lets try to solve one using celery. 
#install celery
pip install celery 

#tasks.py 

from celery import Celery 

app= Celery('tasks', broker='pyamqp://guest:guest@localhost//')

@app.task
def process_notification(notification):
     #Process the notification
     send_notification(notification)

4. Load Balancing: 
Deploy multiple instances of your notification services and utilizes a load balancer to distribute the load evenly. 

Example Using NGINX as a load balancer: 
    upstream notification_servers {
    server server1.example.com;
    server server2 .example.com;
    #Add more server as needed
 }

 server {
    Listen 80;
    server_name notification.example.com; 
   Location/ {
        proxy_pass http://notification_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        #Add other proxy setting as needed 
    }

 }

 5. Database: 
 Lets use NoSQL database like Apache Cassandra or MongoDB since they are designed for scalability and can be able to handle large amounts of data. 

 Example for MongoDB with 'pymongo' library 

 #install pymongo
 pip install pymongo

 from pymongo import MongoClient 
 
 #Connect to MongoDB 
 client= MongoClient('mongodb://localhost:27017/')
 db=client['notification_db]
 collection = db['notification']

 def save_notification(notification):
      #save the notification to the database
      collection.insert_one(notification)

6. Implement the monitoring tools such as Prometheus and Grafana to keep track of system performance.Set up automatic scaling based on metrics like CPU usage, queue length, and database performance. 

      Example of Prometheus Configuration. 
      #prometheus.yml 
      global: 
        scrap_interval: 15s

     scrap_configs: 
         - job_name: 'notification-service'
         static_configs:
targets: [ 'notifications-service: 8000']

7. Rate-limiting implementation 
    #install redis-py 
    pip install redis 

    import redis 
    import time 

    #Connect to Redis 
    redis_client= redis.StrictRedis(host='localhost', port= 6379, db=0)

def rate_limit(key, limit, period):
         current-time = time.time()
         key= f'rate_limit:{key}'
         pipeline= redis_client.pipeline()
          #Remove old entries 
         pipeline.zremrangebyscore(key, '-inf', current_time -period)
         #Add the current entry 
         pipeline.zadd(key, {current_time: current_time})
         #Get the total count 
         pipeline.zcard(key)
         #Execute the pipeline 
         _,_, count = pipleine.excute()
         #Check if the count exceeds the limit
         return count<= limit

8. Error Handling 
         Design a robust error-handling mechanism to deal with failed notifications and ensure reliable delivery. Implement retries, dead-letter queuses, and logging for effective error management. 
          from celery import Celery 
          app= Celery('tasks', broker = 'pyamqp://guest:guest@localhost//')
        app.conf.task_reject_on_worker_lost= True 

    @app.task(bind=True , maz_retries=3, default_retry_delay=60)
        def process_notification(self, notification):
        try: 

    #process the notification 
   send_notification(notification)
   except Exception as exc: 
   #Log the error 
               print(f' Retrying tasks due to exception: {exc}')    
               #Retry the task 
               raise self.retry()

 
...............................................................................................................


QUESTION 3. 
Give examples of different encryption/hashing methods you have come across(one way and two way)and give examples scripts in Python 3 on how to achieve each one of it (20Points)

First of all encryption and hashing are cryptographic techniques used to secure data. Encryption is a two way process, meaning you can encrypt and decrypt the data, while hashing is a one process, making it suitable for password storage and data integrity verification. Lets try to analyse them in detail. 

 1. One Way Hashing: 
 a. MD5 (Message Digest Algorithm 5): 
 MD5 is a widely used hash function producing a 128-bit hash value. 

 Script using hashlib: 
 import hashlib

 def md5_hash(data):
     md5 = hashlib.md5()
     return md5.hexdigest()

#Example Usage 
data_to_hash = "Hello, MD5!"
hashed_data = md5_hash(data_to_hash)    
print(f"MD5 Hash: {hashed_data}")

b. SHA-256(Secure Hash Algorithm 256-bit): 
SHA-256 is a member of the SHA-2 family and produces a 256-bit hash value. 

import hashlib 

def sha256-hash(data): 
    sha256= hashlib.sha256()
    sha256.update(data.encode('utf-8'))
    return sha256.hexdigest()

 #Example Usage 
 data_to_hash = "Hello, SHA_256!" 
 hashed_data = sha256_hash(data_to-hash)   
 print(f"SHA-256 Hash: {hashed_data}")


 2. Two Way Encryption 
 a. Fernet Symmetric Encryption ( AES-128 in CBC model):
 Fernet is a symmetric encryption method provided by the cryptography library in python. It uses AES-128 in CBS MODE for encryption and HMAC for authentication. 

 Example Script using Cryptographic Library

 from cryptography.fernet import Fernet 

 def encrypt(data, key): 
     cipher_suite = Fernet(key)
     encrypted_data = cipher_suite.encrypt(data.encode('utf-8'))
     return encrypted_data 

 def decrypt(encrypted_data, key): 
     cipher_suite = Fernet(key)
     decrypted_data = cipher_suite.decrypt(encrypted_data)
     return decrypted_data.decode('utf-8')

 #Example Usage
 key= Fernet. generate_key()  
 data_to_enrypt = "Hello, Fernet1" 
 encrypted_data = encrypt(data_to_encrpt, key)
 decrypted_data = decrypt(encrypted_data, key)


 print (f"Original Data: {data_to-encrypt}")
 print(f"Enrypted Data: {encrypted_data}")
 print(f"Decypted Data: {decrpted_data}')

 b. RSA Asymmetric Encryption 
 RSA is an asymmetric encryption algorithm widely used for securing data transmission. It uses a pair of public and private keys. 

 Using Scripts in a Cryptography library: 

 from cryptography.hasmat.backends import default_backend 
 from cryptography.hazmat.primitives.asymmetric import rsa, padding
 from cryptography.hazmat.primitives import serialization


 def encrypt_rsa(data, public_key):
     encrypted_data = public_key.encrypt(
        data.encode('utf-8'),
        padding.0AEOP(
            mgf = padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
     )
     return encrypted_data

def decrypt_rsa(enrypted_data, private_key):
    decrypted_data = private_key. decrypt(
        encrypted_data, 
        padding.OAEP(
            mgf=padding. MGF1(algorithm=hashes. SHA256()), 
            algorithm= hashes.SHA256(),
            label=None
        )
    ) 
     return decrypted_data.decode ('utf-8')

#Example Usage 
private_key = rsa.generate_private_key (
    public-exponent= 65537, 
    key_size = 2048, 
    backend = default_backend()
)

public_key = private_key.public_key ()

data_to_enrypt = "Hello. RSA!"
encrpted_data = encrypt_rsa (data_to_encrpt, public_key)
decrypted_data = decrypt_rsa(encrypted_data, private key)

print(f"Original Data: {data_to_encrypt}")
print(f"Encrypted Data: {encrypted_data}")
print(f"Decrypted Data: {encrypted_data}")


SECTION B: 

Number 2:
Create a search and results page using Django and postgreSQL database. The 
Django application should be deployed on uwsgi/nginx webserver and NOT 
the development server. This should also be deployed on a red-hat based 
Linux environment or an alpine docker image container. (60 pts)

SECTION B: 

Number 2:
Create a search and results page using Django and postgreSQL database. The 
Django application should be deployed on uwsgi/nginx webserver and NOT 
the development server. This should also be deployed on a red-hat based 
Linux environment or an alpine docker image container. (60 pts)

The walkthrough will cover creating a Django project, defining a models, setting up the views and templates, integrating PostgreSQL, and deploying the application

  Focused on creating a search and results page using Django and PostrgreSQL database .

  Step 1: Set Up Django Project

  Install Django: 
  pip install django

  ![Alt text](images/Images/project2.jpg)

  create a New Django Project and App 
  
  django-admin startproject djangosearchproject
  cd myproject 
  python manage.py startapp searchapp

  ![Alt text](<images/Images/project 1.jpg>)

 Step 2: Define the Model
 Open 'searchapp' in a text editor 

   from django.db import models 

   class Item(models.Model):
         name=models.CharField(max_length=255)
         description = model.TextField()

   def __str__ (self):
            return self.name
 python manage.py makemigrations
            python manage.py migrate

   Step 3: Create Views and Templates
     Open 'searchapp/views.py' in a text editor 
     create a view to handle the search functionality

  #myapp/views.py 

   from django.shortcuts import render
     from .models import Item 

   def search(request):
          query = request.GET.get('q')
          results = Item.objects.filter(name_-icontains=query)if query else []
          return render(request, 'search_results.html', {'query': query, 'results': results})

   Create 'search-results.html' in the templates folder
    inside the searchapp folder,create a new folder named templates'.
    create a new file named 'search_results.html' and add the HTML codes to display search results. 

   Step 4: Configure the URLS
    open 'myapp/urls.py' in a text editor 

  define the URL patterns for your app

   from django.urls import path 
    from .views import search

  urlpatterns =[
        path('search/', search, name= 'search'),

   Include these URLS in the 'djangosearchproject' and include the URLS from your app

  from django.contrib import admin
    from django.urls import include, path 

  url patterns= [
        path('admin/', admin.site.urls),
        path('searchapp/', include('searchapp.urls')),
    ]
    ]
    
  Step5: Configure PostgreSQL
     install 'psycopg2'

  Update Database Settings in 'djangosearchproject.py'
      Updates the 'DATABASES' configuration to use PostgreSQL.

   #myproject/settings.py
      
  DATABASES = {
        'default':{
            'ENGINE' : 'django.db.backends.postgresql',
            'NAME': 'Opere_inter',
            'USER': 'postgres',
            'PASSWORD': 'brandonopere008', 
            'HOST': 'localhost',
            'PORT': '5432'
        }
      }

Step 6: Test Locally 

python manage.py runserver 

Open the Web browser 
 Go to http://localhost:8000/searchapp/' and test your search page.

 Step 7> Deploy with uWSGI and Nginx
 install uWSGI 

pip install uwsgi 

create a 'uwsgi.ini' File 
Configure uWSGI in a file names 'uwsgi.ini'.

[uwsgi]

module = djangosearchproject.wsgi:application
Configure the Nginx; Install Nginx and configure it to forward requests to uWSGI 

  ![Alt text](images/Images/Project3.jpg)

  Step 8: Deploy with Docker 
  Create a file named 'Dockerfile' to build your docker image 

  # Dockerfile 
  FROM python: 3.8-alpine 

  WORKDIR /APP

  COPY requirements.txt.
  RUN pip install --no-cache-dir -r requirements.txt 

  COPY  .  .
  CMD ["uwsgi", "--ini", "uwsgi.ini"]

  ![Alt text](images/Images/project4.jpg)

Create a requirement.txt File 
List your project dependencies in a file named 'requirements.txt'.

Build and Run Docker Container

docker build -t djangosearchproject 
docker run -p 8000:8000 djangosearchproject 
  ![Alt text](images/Images/project5.jpg)
  ![Alt text](images/Images/project6.jpg)
  Test Your Dockerized App:
  Open a web browser and go to 'http://localhost:8000/searchapp/djangosearchproject/' to esnure everything works. 
 ![Alt text](images/Images/project7.jpg)

This detailed walkthrough covers each step of creating a search and results page using django with PostgreSQL. It includes configuring the databases, creating views and templates , and deploying the application locally and in a docker container. If you have any questions or encounter issues at any step feel free to ask for further clarification. 











