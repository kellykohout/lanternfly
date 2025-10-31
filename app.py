from flask import Flask, request, jsonify, render_template
from azure.storage.blob import BlobServiceClient

# Azure connection info (you can replace with your own)
CONNECTION_STRING = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
CONTAINER_NAME = "lanternfly-images-m5d7nrsb"

# Initialize Azure and Flask
bsc = BlobServiceClient.from_connection_string(CONNECTION_STRING)
cc  = bsc.get_container_client(CONTAINER_NAME)

app = Flask(__name__)

@app.post("/api/v1/upload")
def upload():
    f = request.files["file"]
    blob = cc.get_blob_client(f.filename)
    blob.upload_blob(f, overwrite=True)
    return jsonify(ok=True, url=f"{cc.url}/{f.filename}")

@app.get("/api/v1/gallery")
def gallery():
    blobs = cc.list_blobs()
    urls = [f"{cc.url}/{b.name}" for b in blobs]
    return jsonify(ok=True, gallery=urls)

@app.get("/api/v1/health")
def health():
    return jsonify(ok=True)

@app.get("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)