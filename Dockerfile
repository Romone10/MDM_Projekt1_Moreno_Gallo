# Usage
# docker build -t mosazhaw/hikeplanner .
# docker run --name smartphone -e AZURE_STORAGE_CONNECTION_STRING='DefaultEndpointsProtocol=https;AccountName=gallomor;AccountKey=PU+pUgePeftiCA7K5TN/6aUAbCWIOmKGeM9AMyuQMwLxR/a4uEXXGG1k/3MpsKiesS6oPzMoBdvV+ASt7cmfig==;EndpointSuffix=core.windows.net' -p 9001:80 -d gallomor/smartphone

FROM python:3.10.11

# Copy Files
WORKDIR /usr/src/app
COPY backend/service.py backend/service.py
COPY frontend/build frontend/build

# Install
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Docker Run Command
EXPOSE 80
ENV FLASK_APP=/usr/src/app/backend/service.py
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0", "--port=80"]