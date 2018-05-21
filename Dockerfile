FROM tiangolo/uwsgi-nginx-flask:python3.6

COPY . /app

RUN pip install -r requirements.txt
RUN pip install -r modelling-requirements.txt
