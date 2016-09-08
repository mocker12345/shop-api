FROM daocloud.io/python:2.7
ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN mkdir /code
WORKDIR /code
COPY . /code
COPY docker-entrypoint.sh docker-entrypoint.sh
RUN chmod +x docker-entrypoint.sh
EXPOSE 8000

CMD /code/docker-entrypoint.sh