FROM python:3.8-slim-buster
WORKDIR /app2
#COPY . /app2
#USER root
# COPY . /app
COPY data /app2/data
RUN pip install rasa==3.5.1
#RUN rasa train
#VOLUME actions /app2/actions
COPY models /app2/models
#COPY static /app2/static
COPY config.yml /app2/config.yml
COPY credentials.yml /app2/credentials.yml
COPY domain.yml /app2/domain.yml
COPY endpoints.yml /app2/endpoints.yml
COPY index.html /app2/index.html
COPY test.py /app2/test.py
COPY test_stories.yml /app2/test_stories.yml
EXPOSE 5005
#VOLUME /app/ssl
CMD ["rasa","run","-m","models","--enable-api","--cors","*","--debug" ,"--endpoints", "endpoints.yml", "--log-file", "out.log", "--debug"]
