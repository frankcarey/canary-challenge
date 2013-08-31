INSTALLATION
============

Django REST Framework: http://django-rest-framework.org/

`pip install djangorestframework markdown django-filter`

Install gevent

`brew install libevent`
`pip install gevent`

Install redis
`brew install redis`
`pip install redis`

RUNNING
========

SERVERS
--------

There are 2 servers, one for the django app and one that handles the realtime communication with the devices.To enable the servers:

The django app should run on port 8000

`python website/manage.py runserver`

The realtime server should be running on port 8888
`python server/server-asyncore.py`

Create new devices by going to the django admin:

http://127.0.0.1:8000/admin

When you create the Device, you give it a serial number, which is used for the clients.


CLIENTS
-------

Then after they are running, you can start 'any' number of clients:

`python client/client.py [SERIAL NUMBER]`

Each one will fetch the device id for that serial number from the rest api, and the current privacyMode setting. Then it will register iself with the realtime server. If you change the privacyMode setting in the device admin (or post a REST update for that matter) an event will be published to redis, and forwarded to any registered device.


TODOS
=====
* TESTS
* Error checking! Handling the socket errors, checking for proper values.
* Move the print statements to logger
* More comments
* Check sanity of spawning so many redis clients.
* Use zeromq... everywhere. It should be more robust and handles the message framing for us. It should also mean that we can use worker threads > processes > machines. Would also provide a queue system for spotty wifi without lossing the connection... lots to like http://zero.mq
* Move temp updates to realtime connection. Got the socket open, so we might as well.
* Security - Should be talking over a secure connection (SSL)
* Authentication - No real authentication going on. Considering oauth2, where each machine when registered to a use gets an app id and a token for communication. Users credentials are not stored on machine and they could unregister a maching from the web (like if it was stolen - IRONY!!) 
* Broaden the API so that you could provide other settings like on-off schedule, update notifications, etc.
