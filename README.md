# Invictus Microservice
A small containerised micrsoservice that performs a variety of functions using *nameko*.

Functions:
1. Take a list of integers as input and output a list where every odd number is squared.
2. Take a list of strings as input and output a hashmap where the key is the original string and
the value is the Huffman encoding of that string.
3. Take a Huffman encoded value as input and output the decoded version.

## Setup/Run commands
### Environment setup for testing:
```
virtualenv service_env
source service_env/bin/activate
pip3 install ntlk
pip3 install nameko
pip3 install dahuffman
python3 src/gutenberg_downloader.py
```

### Creating the RabbitMQ server and InvictusService container:
```
docker network create invictus_net   
docker run --network invictus_net -p 5672:5672 --hostname nameko-rabbitmq --name rabbit rabbitmq:3
docker build --tag invictus-service .   
docker run --network invictus_net --name invictus_service invictus-service 
```
### Using the service:
```
nameko shell --config shell_config.yml 
```      
### Starting|Stopping the RabbitMQ server/Invictus Service:
```
docker start|stop rabbit
docker start|stop invictus_service
```

### Testing:
```
pytest test/test.py
```

## Task
Overall the task was fairly simple and straightforward, and took me around 9 hours. The functions that had to be written weren't difficult,
and the Huffman encoder package I found works wonderfully! I was considering using a Huffman encoder I wrote in 3rd
year in C++, but I figured it would just be easier to use a package than to attach C++ code to my python script.

The biggest issue I ran into was actually an error
out of my control. Kombu 4.6.4 broke some part of nameko, but obviously since I only just started using the
system, I thought I had setup something incorrectly. I eventually tried the same code on a linux machine and it worked,
so initallly I thought it was a macos problem. Searching for the error though eventually lead me to the fact that
Kombu 4.6.4 just broke nameko's ability to run, so I downgraded to Kombu 4.6.3 and my code magically started working on my machine.
This took a lot of my time.

The second notable issue I ran into was that the default serialiser for nameko cannot handle raw byte data. Initially I thought
I would be able to just cast the byte data to string and back for use, but in python that seems to be extremely cumbersome. In the
end, after I had spent 30 minutes trying to cast byte data, I decided to simply change the serialiser from the default JSON to pickle.
As specified in the *Design* component of this document, using pickle is also just a better choice in this particular instance.

Finally, I did have some issues containerising my nameko service, although these were fairly minor.
However these were mostly related to my utter lack of knowledge
of Docker. I'd say my biggest hurdle was learning how to create a plain Dockerfile (while sifting through unnecessary
functions like docker-compose; Most tutorials have stuff other than just creating a plain Dockerfile). Installing
NLTK in the container was also initially an issue (as the container doesn't come with gcc to compile libraries), but I found out quickly how to 
rectify the issue. I also spent some time trying to "connect" to the Docker network I created, but soon realised Docker abstracts the network
away and you just connect to the container directly.

### Time Distribution
*Setup + Learning nameko and pytest + Implementing odd_sqaure + Trying to fix kombu* : **4.5 hours** (Thursday)

*Implementing Huffman encoding + Changing the serialiser + Testing the service* : **2 hours** (Friday)

*Fixing Kombu + Learning Docker + Containerising the service* : **2.5 hours** (Sunday)

## Design
### Huffman encoding method
The service uses static Huffman encoding, where the codec is based off one peice of data for all encodings.
This is opposed to dynamic Huffman encoding, where a new codec is created per string. While dynamic encoding
would save more space, you would need to know the specific way decode strings in order to meaningfully provide a decoding service.
For example, the strings "wow" and "212" have the same dynamic huffman encoding, so in order to decode the strings you need the
associated huffman trees as input along with the strings. With static eoncding however, we base the encoding off some corpus specific
to your chosen domain (in this case, I chose the domain to be english sentences). Now if we encode "wow" and "212" the encodings will be 
unique, and the only input that needs to be supplied are the raw bytes. This is more suitable for a decoding "service".

### Using pickle as a serialiser
Huffman encoding produces raw byte data. If the service can only handle strings, it would defeat the point of doing huffman encoding in the first place, as the byte data would have to be converted to string format. Therefore, the service must be able to accept and output raw byte data.

## Pros
* Easy to run programmes in isolated environments (Less likely to break due to system wide updates/changes)
* Easier setup than a virtual machine with improved performance (could run many of these services on a single
machine with easy deployment)
* Simple to use

## Cons
* JSON serialiser is sometimes limiting
* The service class should be stateless, so any objects (such as the huffman encoder), should be scoped outside the class for 
performance reasons
* Not immediately obvious whether rpc or http should be used in any given situation (assuming rpc is mostly for internal calls)
* Docker documentation is great, when you know docker

## Useful Links
Using nameko:
* https://www.toptal.com/python/introduction-python-microservices-nameko

Pickle Serialiser:
* https://stackoverflow.com/questions/55332375/how-to-communicate-binary-data-in-nameko-rpc/55339790#55339790
* https://groups.google.com/forum/#!searchin/nameko-dev/serializer%7Csort:relevance/nameko-dev/tzrWa9bV7Xc/2Y71SsqkBwAJ

Fixing Kombu:
* https://github.com/nameko/nameko/issues/655

Installing GCC in python container:
* https://github.com/docker-library/python/issues/312

Docker stuff:
* https://stackoverflow.com/questions/40563469/connecting-to-rabbitmq-docker-container-from-service-in-another-container
* https://www.youtube.com/watch?v=YFl2mCHdv24
* https://www.wintellect.com/containerize-python-app-5-minutes/
