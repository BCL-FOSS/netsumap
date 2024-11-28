FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive

# Create a user
RUN useradd -m netsumapprobe

# Set working directory for the purpose of this Dockerfile
WORKDIR /home/netsumapprobe

RUN apt-get update \
 && apt-get install --assume-yes --no-install-recommends --quiet \
        software-properties-common \
 && add-apt-repository universe \
 && apt-get update \
 && apt-get install --assume-yes --no-install-recommends --quiet \
        python3 \
        python3-pip \
 && apt-get clean all

RUN apt-get update -y

RUN apt-get upgrade -y

# Copy requirements to the app root
COPY probe_main/requirements.txt ./

# Install dependencies
RUN apt-get install -y \
    git \
    iperf3\
    p0f\
    tshark -y 
  
RUN pip install --no-cache-dir -r requirements.txt --upgrade 

RUN pip install -U redis

# Copy the app into our user root
COPY probe_main/ /home/netsumapprobe/

# Make our entrypoint executable
RUN chmod +x probe_boot.sh 

# Set the user
# USER netsumapprobe
# Set the entrypoint
ENTRYPOINT ["sh", "./probe_boot.sh"]