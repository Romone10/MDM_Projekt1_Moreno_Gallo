# cd backend
# export AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=gallomor;AccountKey=PU+pUgePeftiCA7K5TN/6aUAbCWIOmKGeM9AMyuQMwLxR/a4uEXXGG1k/3MpsKiesS6oPzMoBdvV+ASt7cmfig==;EndpointSuffix=core.windows.net"

# python -m flask --debug --app service run

import datetime
import os
import pickle
from pathlib import Path

import pandas as pd
from azure.storage.blob import BlobServiceClient
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

# init app, load model from storage
print("*** Init and load model ***")
if 'AZURE_STORAGE_CONNECTION_STRING' in os.environ:
    azureStorageConnectionString = os.environ['AZURE_STORAGE_CONNECTION_STRING']
    blob_service_client = BlobServiceClient.from_connection_string(azureStorageConnectionString)

    print("fetching blob containers...")
    containers = blob_service_client.list_containers(include_metadata=True)
    for container in containers:
        existingContainerName = container['name']
        print("checking container " + existingContainerName)
        if existingContainerName.startswith("smartprix-model"):
            parts = existingContainerName.split("-")
            print(parts)
            suffix = 1
            if (len(parts) == 3):
                newSuffix = int(parts[-1])
                if (newSuffix > suffix):
                    suffix = newSuffix

    container_client = blob_service_client.get_container_client("smartprix-model-" + str(suffix))
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        print("\t" + blob.name)

    # Download the blob to a local file
    Path("../model").mkdir(parents=True, exist_ok=True)
    download_file_path = os.path.join("../model", "GradientBoostingRegressor.pkl")
    print("\nDownloading blob to \n\t" + download_file_path)

    with open(file=download_file_path, mode="wb") as download_file:
         download_file.write(container_client.download_blob(blob.name).readall())

else:
    print("CANNOT ACCESS AZURE BLOB STORAGE - Please set connection string as env variable")
    print(os.environ)
    print("AZURE_STORAGE_CONNECTION_STRING not set")    

file_path = Path(".", "../model/", "GradientBoostingRegressor.pkl")
with open(file_path, 'rb') as fid:
    model = pickle.load(fid)

OS_Android = True
Display_60Hz = False
Display_120Hz = True
Battery_mAh = 5000
RAM_GB = 8.0
GHz = 2.8
Has_5G = True
Dual_Sim = True




print("*** Init Flask App ***")
app = Flask(__name__)
cors = CORS(app)
app = Flask(__name__, static_url_path='/', static_folder='../frontend/build')

@app.route("/")
def indexPage():
     return send_file("../frontend/build/index.html")  

@app.route("/api/predict", methods=['POST'])
def predict():     
    data = request.json     
    OS_Android = data['OS_Android']     
    Display_60Hz = data['Display_60Hz']     
    Display_120Hz = data['Display_120Hz']     
    Battery_mAh = data['Battery_mAh']     
    RAM_GB = data['RAM_GB']     
    GHz = data['GHz']     
    Has_5G = data['Has_5G']     
    Dual_Sim = data['Dual_Sim']          
    input_data = [[OS_Android, Display_60Hz, Display_120Hz, Battery_mAh, RAM_GB, GHz, Has_5G, Dual_Sim]]
    prediction = model.predict(input_data)[0]     
    
    return jsonify({'price': str(prediction)}) 
if __name__ == "__main__":     
    app.run(debug=True)
