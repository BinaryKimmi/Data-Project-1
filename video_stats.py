import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path = "./.env")

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = "MrBeast"
maxResults = 50


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
        #print(channel_playlistId)
        return channel_playlistId
    
    ###any exceptions encountered will be saved to the variable e
    except requests.exceptions.RequestException as e:

        ###In Python, raise e is used within an except block to re-raise the caught exception, preserving its original traceback. 
        ###This is a key mechanism for exception handling, allowing you to perform actions (like logging) and then propagate the error up the call stack. 
        raise e


def get_video_ids(playlistId):
    
    video_ids = []
    pageToken = None
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlistId}&key={API_KEY}"
    try:
        while True:
            url = base_url
            if pageToken:
                url += f"&pageToken={pageToken}"

            response = requests.get(url)

            response.raise_for_status()

            data = response.json()

            for item in data.get('items', []):
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)

            #Get Next Page
            pageToken = data.get('nextPageToken')

            #break out for loop if page token isnt found
            if not pageToken:
                break

        return video_ids

            ###print in json format
           
    except requests.exceptions.RequestException as e:
        raise e


def extract_video_data(video_ids):

    extracted_data = []

    def batch_list(video_id_list, batch_size):
    ###Will loop through the list in batches of size-batch_size 
        for video_id in range(0, len(video_id_list), batch_size):
            yield video_id_list[video_id: video_id + batch_size]

    ##Loop through the entire list in batches, at each batch concatenate
    try:
        for batch in batch_list(video_ids, maxResults):
            video_ids_str = ",".join(batch)

            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}" 

            response = requests.get(url)

            response.raise_for_status()

            ###print in json format
            data = response.json()

            for item in data.get('items',[]):
                video_id = item['id']
                snippet = item['snippet']
                contentDetails = item['contentDetails']
                statistics = item['statistics']

            ##Define data dictionary that will take data from the above loop
                video_data = {
                    "video_id": video_id,
                    "title": snippet["title"],
                    "publishedAt": snippet["publishedAt"],
                    "duration": contentDetails["duration"],
                    ##The None is if there are videos with no stated attributes, then just put "none"
                    "viewCount": statistics.get("viewCount", None),
                    "likeCount": statistics.get("likeCount", None),
                    "commentCount": statistics.get("commentCount", None),
                }

                extracted_data.append(video_data)

        return extracted_data
    
    except requests.exceptions.RequestException as e:
        raise e





###Before running a Python file, the interpreter sets a few special variables. O
### One of them is __name__. If a Python file is run directly, Python sets __name__ to "__main__".
###If the same file is imported into another file, __name__ is set to the module’s name.
### The condition if __name__ == "__main__": evaluates to False, and the code block is skipped. 
###This allows you to control which parts of the code execute in different contexts. 

if __name__ == "__main__":
    playlistId = get_playlist_id()
    video_ids = get_video_ids(playlistId)
    print(extract_video_data(video_ids))
    #print(get_video_ids(playlistId))


