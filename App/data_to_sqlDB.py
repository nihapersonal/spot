from azure.storage.filedatalake import DataLakeServiceClient
import pyodbc
import os
from dotenv import load_dotenv
import textwrap
import datetime
from azure.storage.blob import BlobSasPermissions

load_dotenv()

##Establishing a connection with SQL server database

#specify the server name, database name, username and password
server_name = os.getenv('server_name') 
database_name = os.getenv('database_name')
username = os.getenv('uname')
password = os.getenv('password')

#create a full connection string
connection_string = f"DRIVER={{ODBC Driver 17 for SQL server}};SERVER={server_name};DATABASE={database_name};UID={username};PWD={password};connection Timeout={30}"

#create a PYODBC connection object.
conn = pyodbc.connect(connection_string)

#create a new cursor object from the connection
cursor = conn.cursor()

##Establishing a connection with the datalake storage

from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
import pandas as pd

#enter credentials
account_name = os.getenv("AZURE_STORAGE_NAME")
account_key = os.getenv("account_key")
container_name = 'landing'

#create a client to interact with blob storage
connect_str = 'DefaultEndpointsProtocol=https;AccountName=' + account_name + ';AccountKey=' + account_key + ';EndpointSuffix=core.windows.net'
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

#use the client to connect to the container
container_client = blob_service_client.get_container_client(container_name)

# Retrieve the latest blob
latest_blob = max(container_client.list_blobs(), key=lambda x: x.last_modified)
latest_blob_name = latest_blob.name

import datetime
# Generate a shared access signature for the latest blob
sas_i = generate_blob_sas(account_name=account_name,
                          container_name=container_name,
                          blob_name=latest_blob_name,
                          account_key=account_key,
                          permission=BlobSasPermissions(read=True),
                          expiry=datetime.datetime.utcnow() + datetime.timedelta(hours=1))

sas_url = f'https://{account_name}.blob.core.windows.net/{container_name}/{latest_blob_name}?{sas_i}'

df = pd.read_csv(sas_url)
#print(df)
## Write data to the database

table_name = 'dbo.raw'

# Add ingestion date time column to DataFrame
df['INGESTION_DTTM'] = datetime.datetime.now()
df['RAW_FILE_NAME'] = latest_blob_name

# Convert DataFrame rows to tuples
rows = [tuple(row) for row in df.itertuples(index=False)]

# Prepare the query with parameter placeholders
columns = ', '.join(df.columns)
placeholders = ', '.join(['?' for _ in range(len(df.columns))])
insert_query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
#print(insert_query)

# Execute the insert query with the list of tuples
cursor.executemany(insert_query, rows)
conn.commit()