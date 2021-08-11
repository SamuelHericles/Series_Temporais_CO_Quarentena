FROM ubuntu:latest
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get upgrade &&\
    apt-get update &&\
    apt-get install -y --no-install-recommends \
    unixodbc-dev \
    unixodbc \
    libpq-dev \
    build-essential python3.9 python3-pip python3-dev && \
    pip3 -q install pip --upgrade

RUN mkdir home/app
COPY . home/app
WORKDIR home/app

RUN pip install -r requirements.txt
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]