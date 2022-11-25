FROM python:3.10
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]

# docker build
#  docker build -t rest-apis-flask-python . ### docker build -t [name of docker]

# docker run
#  docker run -dp 5005:5000 rest-apis-flask-python  ### docker run -p [local port]:[docker port] [name of docker]

# this way support real time change code on the local code
# docker run -dp 5005:5000 -w /app -v "$(pwd):/app" flask-smorest-api
### docker run -p [local port]:[docker port] [-w /app means work in this app] ["$(pwd):/app" means from pwd copy to /app in docker] [name of docker]
