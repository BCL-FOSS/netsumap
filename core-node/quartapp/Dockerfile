FROM nvcr.io/nvidia/tensorflow:24.01-tf2-py3

# Create a user
RUN adduser quart --disabled-password 
# Set working directory for the purpose of this Dockerfile
WORKDIR /home/quart

RUN apt-get update -y

RUN apt-get upgrade -y

RUN apt install python3.10-venv -y

# Copy requirements to the app root
COPY quartapp/requirements.txt ./
# Create a virtual environment and install the dependecies
RUN python3 -m venv venv && \
  venv/bin/pip install --no-cache-dir -r requirements.txt --upgrade && \
  chown -R quart:quart ./

# Copy the app into our user root
COPY quartapp/ /home/quart/
# Make our entrypoint executable
RUN chmod +x netsumap_boot.sh

# Set the user
USER quart
# Set the entrypoint
ENTRYPOINT ["sh", "./netsumap_boot.sh"]