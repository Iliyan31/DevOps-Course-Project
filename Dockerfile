# The base image
FROM ubuntu:latest

# Install python and pip
RUN apt-get update && apt-get install -y python3 python3-pip python3-dev build-essential && apt clean

# Copy files required for the app to run
COPY ./src/app.py /usr/src/app/

# Declare the port number the container should expose
EXPOSE 5000

# Run the application
CMD ["python3", "/usr/src/app/app.py"]
