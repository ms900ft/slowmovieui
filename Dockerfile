FROM python:3.8-slim-buster

WORKDIR /python-docker

RUN apt update && apt install -y gcc libffi-dev libssl-dev zlib1g-dev \
  libjpeg-dev  ffmpeg\
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip setuptools
RUN pip3 install -r requirements.txt

COPY . .
RUN cd /python-docker/e-paper/RaspberryPi\&JetsonNano/python && python setup.py install

CMD [ "python3", "slowmovie2.py" "-i 20" "-d 60" "-b 2" -"w"]

