# Importing Packages
from googleapiclient.discovery import build
import pandas as pd
import pickle
import datetime
import base64
from google.cloud import storage
import os
from dotenv import load_dotenv

# Define variables for Cloud Functions
bucket_name = 'youtube_analytics_bucket'
project_name = 'angular-expanse-405413'
api_key = os.getenv('API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)

def main():

    # Creating data
    configure()
    
    current_video_ids = grab_list_generator()

    current_video_stats_df = get_video_stats(youtube, current_video_ids)

    # Convert the DataFrame to a CSV string
    csv_string = current_video_stats_df.to_csv(index=False)

    # Get the current time
    today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Upload CSV file to Cloud Storage
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(f'cloud_function_data/youtube_video_data_{today}.csv')
    blob.upload_from_string(csv_string, content_type='text/csv')

# Retrieving Secure API
def configure():
    load_dotenv()

# Getting list of playlist ids
def chosen_playlist_ids():
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob('chosen_playlist_ids.pkl')
    with blob.open('rb') as file:
        playlist_ids = pickle.load(file)
    return playlist_ids 

# Getting base list of video ids
def get_base_list():
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob('base_video_id_list.pkl')
    with blob.open('rb') as file:
        base_list = pickle.load(file)
    return base_list 

# Getting running collection of day 1 - day7+ video ids list
def get_grab_list():
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob('grab_list.pkl')
    with blob.open('rb') as file:
        grab_list = pickle.load(file)
    return grab_list 

# Function to generate grab list each day
def grab_list_generator():

    # Establishing base lists:
    playlist_ids = chosen_playlist_ids()
    base_list = get_base_list()
    grab_list = get_grab_list()

    # Generating videoID list:
    video_id_list = mass_video_ids(youtube, playlist_ids)

    # Checking for new videos and adding to grab list:
    video_id_checker(base_list, grab_list, video_id_list)

    # Saving new grab list:
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob('grab_list.pkl')
    with blob.open('wb') as file:
        pickle.dump(grab_list, file)

    return grab_list

# Function to get video ids from youtube, which generates new list everyday
def mass_video_ids(youtube, wanted_playlist_ids):

    all_data = []

    for id in wanted_playlist_ids:
        
        nextpage = True
        page = None

        while nextpage:
        # request for first page of playlist
            request = youtube.playlistItems().list(
                part='contentDetails',
                playlistId = id,
                maxResults=50,
                pageToken=page)
            # dictionary of the first page   
            response = request.execute()

        # Accessing videos ids on that first page
            for i in range(len(response['items'])):
                data = dict(playlist_id = id,
                    video_id = response['items'][i]['contentDetails']['videoId'])
                all_data.append(data)

            # Checking to see if there is a next page
            if 'nextPageToken' in response:
                page = response['nextPageToken']              

            else:
                nextpage = False

    # new day df
    all_data_df = pd.DataFrame(all_data)

    retrived_video_ids = all_data_df['video_id']

    return retrived_video_ids

# Identifies post day 0 videos
def video_id_checker(base_list, grab_list, new_list):

    # Iterates through the new list of videoIDs
    for video_id in new_list:
        # Checks if already in base_list
        if video_id in base_list:
            continue
        # Checks if already in grab_list
        elif video_id in grab_list:
            continue
        # Adds to grab list if not already in base_list or grab_list
        else:
            grab_list.append(video_id)

# Function to retrieve the current time
def get_current_time():
    today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return today

# gets all new video data for each video
def get_video_stats(youtube, list_of_video_ids):

    all_data = []

    time = get_current_time()

    # Will only return 50 results at a time, this for loop will do 50 Video IDs at a time
    for i in range(0, len(list_of_video_ids), 50):     

        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(list_of_video_ids[i:i+50]))

        response = request.execute()

        for video in response['items']:
  
            data = dict(video_id = video['id'],
                        channel_id = video['snippet']['channelId'],
                        published_at = video['snippet'].get('publishedAt'),
                        title = video['snippet'].get('title'),
                        description = video['snippet'].get('description'),
                        tags = video['snippet'].get('tags', []),
                        category_id = video['snippet'].get('categoryId'),
                        duration = video['contentDetails'].get('duration'),
                        caption = video['contentDetails'].get('caption'),
                        licensed_content = video['contentDetails'].get('licensedContent'),
                        default_language = video['snippet'].get('defaultLanguage'),
                        content_rating = video['contentDetails'].get('contentRating'),
                        view_count = video['statistics'].get('viewCount'),
                        like_count = video['statistics'].get('likeCount'),
                        favourite_count = video['statistics'].get('favoriteCount'),
                        comment_count = video['statistics'].get('commentCount'),
                        extraction_date = time)

            all_data.append(data)

    all_data_df = pd.DataFrame(all_data)

    return all_data_df

def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print(pubsub_message)
    main()

if __name__ == "__main__":
    hello_pubsub('data', 'context')