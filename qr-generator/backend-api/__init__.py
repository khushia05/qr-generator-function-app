import logging
import azure.functions as func
import qrcode
import io
import os
from azure.storage.blob import BlobServiceClient, ContentSettings
from datetime import datetime

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('QR Function triggered.')

    data = req.params.get('data')
    if not data:
        return func.HttpResponse("Please pass 'data' query string", status_code=400)

    # Generate QR code image
    img = qrcode.make(data)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    # Define blob name using timestamp
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    blob_name = f"qr_{timestamp}.png"

    try:
        # Get connection string and container name from environment variables
        conn_str = os.environ["AzureWebJobsStorage"]
        container_name = os.environ.get("QR_CONTAINER_NAME", "qr-codes")

        # Upload to Azure Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string(conn_str)
        container_client = blob_service_client.get_container_client(container_name)

        # Create container if it doesn't exist
        if not container_client.exists():
            container_client.create_container()

        # Upload image
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(
            buf,
            blob_type="BlockBlob",
            overwrite=True,
            content_settings=ContentSettings(content_type='image/png')
        )

        # Create blob URL
        blob_url = blob_client.url
    
        return func.HttpResponse(
        f"""
        <html>
            <body style="text-align:center; font-family:Arial;">
                <h2>QR Code Generated Successfully!</h2>
                <a href="{blob_url}" target="_blank" download>📥 Download QR Code</a><br><br>
                <img src="{blob_url}" alt="QR Code" style="width:200px; height:200px; margin-top:10px;" />
            </body>
        </html>
        """,
        mimetype="text/html" 
        )

    except Exception as e:
        logging.error(f"Upload failed: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)