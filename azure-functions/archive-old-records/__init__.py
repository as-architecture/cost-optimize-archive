import datetime, os
import azure.functions as func
from azure.cosmos import CosmosClient
from azure.storage.blob import ContainerClient
import pandas as pd

HOT_DB = "BillingDB"
HOT_CONTAINER = "Records"
COLD_CONTAINER = "ColdBlobs"
CUTOFF_DAYS = 90

client = CosmosClient(os.getenv("COSMOS_URI"), os.getenv("COSMOS_KEY"))
hot_cont = client.get_database_client(HOT_DB).get_container_client(HOT_CONTAINER)
blob_cli = ContainerClient.from_connection_string(
        os.getenv("BLOB_CONN"), container_name=COLD_CONTAINER)

def main(mytimer: func.TimerRequest):
    cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=CUTOFF_DAYS)
    query = f"SELECT * FROM c WHERE c.timestamp < '{cutoff.isoformat()}Z'"
    old_items = list(hot_cont.query_items(query=query, enable_cross_partition=True))
    if not old_items:
        return
    df = pd.DataFrame(old_items)
    blob_name = f"archive/{cutoff.date().isoformat()}_{len(df)}.parquet"
    df.to_parquet("/tmp/data.parquet", index=False)
    with open("/tmp/data.parquet", "rb") as f:
        blob_cli.upload_blob(name=blob_name, data=f)
    for item in old_items:
        hot_cont.delete_item(item, partition_key=item["pk"])