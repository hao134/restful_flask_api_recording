# Docker E-book:
https://rest-apis-flask.teclado.com/docs/docker_intro/in_depth_docker_tutorial/

# run Docker
 
## docker build
```
docker build -t rest-apis-flask-python . ### docker build -t [name of docker]
```

## docker run
```
docker run -dp 5005:5000 rest-apis-flask-python   
```
### explain:
docker run -p [local port]:[docker port] [name of docker]

## this way support change local code and reply to docker code real time 
```
docker run -dp 5005:5000 -w /app -v "$(pwd):/app" flask-smorest-api
```
### explain
docker run -p [local port]:[docker port] [-w /app means work in this app] ["$(pwd):/app" means from pwd copy to /app in docker] [name of docker]

ref: https://blog.teclado.com/python-dictionary-merge-update-operators/

## JWT
https://rest-apis-flask.teclado.com/docs/flask_jwt_extended/how_is_jwt_used/
### Getting an access token
* The client sends authentication information to the API (usually, username and password)
* The API validates them and generates an access token (in our case, a JWT)
* Inside the JWT, the user's unique ID is stored.
* The access token is sent back to the client for storage and later use.
![](https://i.imgur.com/Y5MtiRK.png)
  
### An example of using access tokens
* Imagine you're making an API with an endpoint, /my-info, which should return information about the currently logged-in user
* Imagine the client is a website. In the website there is a button, "See my info", which when clicked sends a request to /my-info to get the information.
* Let's say a user arrives at the website without having logged in. What does the flow look like?
![](https://rest-apis-flask.teclado.com/assets/images/my-info-flow.drawio-e9ca9f4a6cb7789c88884321fdcdcba8.png)