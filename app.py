import os
import flask
from flask import Flask, request, jsonify
from azure.storage.blob import BlobServiceClient, BlobPrefix

app = Flask(__name__)

# Set your Azure Storage account information
account_name = os.environ["STORAGE_ACCOUNT_NAME"]
account_key = os.environ["STORAGE_ACCOUNT_KEY"]
container_name = os.environ["CONTAINER_NAME"]

# Initialize the BlobServiceClient
blob_service_client = BlobServiceClient(
    account_url=f"https://{account_name}.blob.core.windows.net",
    credential=account_key
)
container_client = blob_service_client.get_container_client(container_name)


@app.route('/query', methods=['GET'])
def query_storage_container():
    try:
        # Query the contents of the Azure Storage container
        blobs = list(container_client.list_blobs(name_starts_with=request.args.get('prefix', '')))

        # Extract relevant information from each blob
        blob_info = []
        for blob in blobs:
            blob_info.append({
                'name': blob.name,
                'last_modified': blob.last_modified,
                'size': blob.size
            })

        return jsonify({'blobs': blob_info})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

