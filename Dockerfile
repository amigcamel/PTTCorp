FROM python:2.7.9
ENV HOME /pttcorp
WORKDIR $HOME
ADD . $HOME
RUN pip install -r pip.txt uwsgi
CMD ["uwsgi", "--uid", "root", "--master", "--http", "0.0.0.0:8002", "--module", "PTTCorp.wsgi", "--static-map", "/static_pttcorp=static_pttcorp",  "--process", "2"]

