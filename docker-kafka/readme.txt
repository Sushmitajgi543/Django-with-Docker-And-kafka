models.py
------

create customuser using ---from django.contrib.auth.models import AbstractUser
create book using ---from django.db import models ,(models.Model)

----

setting.py
------
add app in installed app
add AUTH_USER_MODEL = appname.customeruser

--
admin.py
------
resgister customer user
add customer user

----
migration file
python manage.py makemigration appanem
python manage.py migrate


------
create superuser

create superuser to access admin panel -- python manage.py createsuperuser (locally)

in docker
--docker exec -it authentication-web-1 /bin/bash
--python manage.py createsuperuser


-- docker-compose up --build , -d  ,down

----------------------------------------------
KAFKA
----------
1. pip install confluent-kafka
2. add # settings.py
KAFKA_BROKER = 'localhost:9092'
3. create a file producers.py
4. create a file consumers.py
5. locally run consumer =  1. pythonw consumer.pyw  ,,, 2. start python consumer.py
   docker ---

   # Connect to Kafka container
docker exec -it <your_project_name>_kafka_1 /bin/bash

# Create a Kafka topic
kafka-topics.sh --create --topic test-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

# Produce a message to the topic
kafka-console-producer.sh --topic test-topic --bootstrap-server localhost:9092
write msessage than ctrl+c

# Consume messages from the topic
kafka-console-consumer.sh --topic test-topic --from-beginning --bootstrap-server localhost:9092

python producers.py
python consumers.py


--------------
# FOR KUBER NETES
------------
Build and Push Docker Image:
1. docker build -t authentication-web-1:tag1 .
2.docker push your-docker-image:tag


