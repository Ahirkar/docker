FROM python:3.8-slim-buster
WORKDIR /nick
# Install system dependencies
RUN apt-get update && apt-get install -y libgomp1
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y
# Copy files to the working directory
COPY requirements.txt .
COPY api.py .
COPY utilities.py .
COPY tmp.jpg .
COPY data .
RUN pip install pymongo
# Install Python dependencies
RUN pip install -r requirements.txt
EXPOSE 5006
# Set command to run
CMD ["python", "api.py"]

