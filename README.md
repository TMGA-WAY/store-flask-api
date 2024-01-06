To build the image-
```commandline
    docker build -t rest-api-flask-python .
```
To run the docker container-
```commandline
    docker run -p 4500:4500 rest-api-flask-python
```
To run in background
```commandline
    docker run -d -p 4500:4500 rest-api-flask-python
```

To run in development mode in background
```commandline
    docker run -d -p 4500:4500 -w /app -v "$(pwd):/app" rest-api-flask-python
```