FROM ubuntu:22.04

RUN apt update -y && apt install -y python3 python3-pip python3-dev cython3 git make

WORKDIR /usr/src

RUN git clone https://github.com/hzeller/rpi-rgb-led-matrix/
RUN cd rpi-rgb-led-matrix/bindings/python && make build-python  PYTHON=$(which python3) && make install-python PYTHON=$(which python3)

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN python3 -m pip install -r requirements.txt

# copy project
COPY . /usr/src/app/

ENTRYPOINT ["python3", "app.py"]
