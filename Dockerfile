FROM python:3.11

RUN mkdir -p /usr/src/app

COPY ./requirements.txt /usr/src/app

COPY ./upbit_module.py /usr/src/app

COPY ./main.py /usr/src/app

COPY ./.env /usr/src/app

RUN pip install --upgrade pip

RUN pip install pyupbit

RUN pip install -r requirements.txt

RUN python main.py


