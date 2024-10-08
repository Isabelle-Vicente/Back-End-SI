from azure.storage.blob import BlobServiceClient
from django.conf import settings

def upload_image_to_azure(file, filename):
    blob_service_client = BlobServiceClient(
        account_url=f"https://{settings.AZURE_ACCOUNT_NAME}.blob.core.windows.net",
        credential=settings.AZURE_ACCOUNT_KEY
    )
    container_client = blob_service_client.get_container_client(settings.AZURE_CONTAINER)
    blob_client = container_client.get_blob_client(blob=filename)
    blob_client.upload_blob(file, overwrite=True)
    return blob_client.url
