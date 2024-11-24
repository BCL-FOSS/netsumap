FROM ubuntu:22.04

# Create a user
RUN useradd -m quart

# Set working directory for the purpose of this Dockerfile
WORKDIR /home/quart

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
COPY quartapp/requirements.txt ./

# Install dependencies
RUN apt-get install -y \
    git \
    iperf3 \
    p0f \
    tshark
  
RUN pip install --no-cache-dir -r requirements.txt --upgrade 

# Copy the app into our user root
COPY quartapp/ /home/quart/

# Make our entrypoint executable
RUN chmod +x probe_boot.sh 

# Set the user
# USER quart
# Set the entrypoint
ENTRYPOINT ["sh", "./probe_boot.sh"]