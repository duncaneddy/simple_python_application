FROM ubuntu:bionic

# Update Ubuntu Image
RUN apt-get update
RUN apt-get upgrade -y

# Install Python
RUN apt install -y python3-dev python3-pip
RUN pip3 install -U pip

# Copy application and install
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN pip3 install .

# Expose application ports
EXPOSE 9999

CMD ["python3", "./simple_app/app.py"]