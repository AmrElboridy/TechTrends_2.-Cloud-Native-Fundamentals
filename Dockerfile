# Set the base image. 
FROM python:3.8
# Set a key-value label 
LABEL maintainer="Amr ElBoridy"
# This container listens for traffic on the 3111 port
EXPOSE 3111
# Copy files from the host to the container filesystem. 
COPY . /app
# Define  working directory 
WORKDIR /app
# Run commands to install dependencies and 
RUN pip install -r ./techtrends/requirements.txt
# Ensure that the database is initialized 
RUN  python ./techtrends/init_db.py
# Command to run on container start. 
CMD [ "python", "./techtrends/app.py" ]