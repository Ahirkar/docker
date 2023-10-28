FROM python:3.8-slim-buster
WORKDIR /app
#./data /app/data
#COPY ./actions /app/actions
#COPY ./actions/requirements.txt /app/actions/requirements.txt
#COPY _init_.py .
COPY actions.py /app/actions.py
COPY Constant.py /app/Constant.py
COPY dbcheck.py /app/dbcheck.py
COPY requirements.txt /app/requirements.txt
USER root
#RUN python -m pip install --upgrade pip
RUN pip install -r /app/requirements.txt
#Copy /actions /app/actions
EXPOSE 5055
CMD ["rasa" ,"run" ,"actions"]
