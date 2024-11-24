FROM ubuntu:latest

# Create a user
RUN useradd -m quart

# Set working directory for the purpose of this Dockerfile
WORKDIR /home/quart

RUN apt-get update -y

RUN apt-get upgrade -y

# Install dependencies for building libpcap and other tools
RUN apt-get install -y \
    git \
    build-essential \
    libtool \
    automake \
    autoconf \
    iperf3 \
    p0f \
    tshark \
    python3-pip 

# Install libpcap for rpcapd
RUN git clone https://github.com/the-tcpdump-group/libpcap.git /tmp/libpcap && \
    cd /tmp/libpcap 
RUN ./configure --enable-remote
RUN make
RUN make install
RUN cd / && rm -rf /tmp/libpcap

# Copy requirements to the app root
COPY quartapp/requirements.txt ./

# Install pip dependencies
RUN pip install --no-cache-dir -r requirements.txt --upgrade 

# Copy the app into our user root
COPY quartapp/ /home/quart/

# Make our entrypoint executable
RUN chmod +x probe_boot.sh 

# Set the user
# USER quart
# Set the entrypoint
ENTRYPOINT ["sh", "./probe_boot.sh"]