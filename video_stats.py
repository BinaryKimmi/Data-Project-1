import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path = "./.env")

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = "MrBeast"


def get_playlist_id():
    try:
    #URL for request
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"

        response = requests.get(url)
        response.raise_for_status()

        ###print in json format
        data = response.json()
        #print(json.dumps(data,indent=4))

        channel_items = data['items'][0]

        channel_playlistId = channel_items['contentDetails']['relatedPlaylists']['uploads']

        ###PlaylistID
        print(channel_playlistId)
        return channel_playlistId
    
    ###any exceptions encountered will be saved to the variable e
    except requests.exceptions.RequestException as e:

        ###In Python, raise e is used within an except block to re-raise the caught exception, preserving its original traceback. 
        ###This is a key mechanism for exception handling, allowing you to perform actions (like logging) and then propagate the error up the call stack. 
        raise e





###Before running a Python file, the interpreter sets a few special variables. O
### One of them is __name__. If a Python file is run directly, Python sets __name__ to "__main__".
###If the same file is imported into another file, __name__ is set to the module’s name.
### The condition if __name__ == "__main__": evaluates to False, and the code block is skipped. 
###This allows you to control which parts of the code execute in different contexts. 

if __name__ == "__main__":
    #print("get_playlist_id will be executed")
    get_playlist_id()
#else:
#    print("get_playlist_id wwont be executed")
