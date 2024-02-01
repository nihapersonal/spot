import webbrowser
from flask import Flask, request
import spotipy
from spotipy import oauth2
import pandas as pd
from dotenv import load_dotenv
import os
import os, uuid
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient

app = Flask(__name__)


load_dotenv()

@app.route('/callback')
def callback():
    response_url = request.url
    print('Received response URL:', response_url)
    return 'Authorization successful! You can close this page now.'

if __name__ == '__main__':
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    redirect_uri = 'https://open.spotify.com/' 

# Define the required scopes
    scope = 'user-read-recently-played'
    sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope)
    auth_url = sp_oauth.get_authorize_url()

    response_url= print('Please visit this URL to authorize the application: ', auth_url)

    # Automatically open the authorization URL in the web browser
    #webbrowser.open(auth_url, new=2)

    # Start the local Flask web server to handle the redirect URI
    app.run(port=8888)

# Extract the authorization code from the URL
code = sp_oauth.parse_response_code(response_url)

# Exchange the authorization code for an access token
token_info = sp_oauth.get_access_token(code)
access_token = token_info['access_token']

# Create a Spotipy client using the access token
sp = spotipy.Spotify(auth=access_token)

# Retrieve the recently played tracks
results = sp.current_user_recently_played(limit=40)  # Adjust the limit as per your needs

# Create a Spotipy client using the access token
sp = spotipy.Spotify(auth=access_token)

# Retrieve the recently played tracks
results = sp.current_user_recently_played(limit=40)  # Adjust the limit as per your needs

song_names = []
artist_names = []
played_at_list = []
timestamps = []

def return_dataframe(): 
# Process the response
    tracks =[]
    for song in results["items"]:
          song_names.append(song["track"]["name"])
          artist_names.append(song["track"]["album"]["artists"][0]["name"])
          played_at_list.append(song["played_at"])
          timestamps.append(song["played_at"][0:10])
          
#Prepare a dictionary in order to turn it into a pandas dataframe below       
    song_dict = {
          "song_name" : song_names,
          "artist_name" : artist_names,
          "played_at" : played_at_list,
          "played_on_date" : timestamps
      }
    song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "played_at", "played_on_date"])
    return song_df

data = return_dataframe()

#getting the connection string
connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

# Instantiate a new BlobServiceClient using a connection string
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

# Set the name of the containers
container_name = "landing"

#set the name of the blob
#blob_name = "song_data"

# Create the container if it doesn't exist
container_client = blob_service_client.get_container_client(container_name)

# If the container doesn't exist, create it
if not container_client.exists():
    container_client.create_container()

# Generate a unique blob name
def generate_blob_name(base_name, num):
    return f"{base_name}_{num:02}"

base_blob_name = "recently_played_songs"

# Read the current blob number from a file or default to 1 if the file doesn't exist
try:
    with open("current_blob_number.txt", "r") as file:
        current_blob_number = int(file.read())
except FileNotFoundError:
    current_blob_number = 1

# Generate the blob name
blob_name = generate_blob_name(base_blob_name, current_blob_number)

# Increment the current blob number for the next run
current_blob_number += 1

# Write the updated current blob number back to the file
with open("current_blob_number.txt", "w") as file:
    file.write(str(current_blob_number))

# Convert the DataFrame to a CSV string
    csv_data = data.to_csv(index=False)

# Upload the CSV string as a blob
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(csv_data)