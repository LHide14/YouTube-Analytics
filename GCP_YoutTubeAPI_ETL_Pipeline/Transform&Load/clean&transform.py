import pandas as pd
from google.cloud import storage
import os
from dotenv import load_dotenv
import io
from googleapiclient.discovery import build
from datetime import timedelta, datetime
import datetime

# YouTube API Connection
load_dotenv()
api_key = os.getenv('API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)

# Google Storage
bucket_name = os.getenv('BUCKET_NAME')
folder_path = os.getenv('FOLDER_PATH')
project_name = os.getenv('PROJECT_NAME')
running_data_folder = os.getenv('RUNNING_DATA_FOLDER')
client = storage.Client()
blobs = client.list_blobs(bucket_name, prefix=folder_path)

def main():
    # Getting Running Data
    running_df = get_running_df()
    # Getting New Data
    new_data = get_todays_csv()
    # Merge and Clean with Running Data
    running_df = merge_clean_function(running_df, new_data)
    # Save New DF
    save_data(running_df)


def get_running_df():

    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob('YouTube_Running_Data/running_youtube_video_data.csv')
    running_csv = blob.download_as_string()
    running_df = pd.read_csv(io.BytesIO(running_csv), encoding='utf-8')

    return running_df

def get_todays_csv():

    today_csv = [blob for blob in blobs][-1]
    csv_file = today_csv.download_as_string()
    df = pd.read_csv(io.BytesIO(csv_file), encoding='utf-8')

    return df

def clean(data):

    # Dealing with Nulls
     # String Columns
    data.title.fillna('', inplace=True)
    data.description.fillna('', inplace=True)

     # Count Columns
    data.comment_count.fillna(0, inplace=True)
    data.view_count.fillna(0, inplace=True)
    data.like_count.fillna(0, inplace=True)
    
    # Columns to String
    columns_to_str = ['video_id', 'channel_id', 'title', 'description']

    for column in columns_to_str:
        data[column] = data[column].astype('string')

    # Object to Int
    columns_to_int = ['view_count', 'like_count', 'comment_count']

    for column in columns_to_int:
        data[column] = data[column].astype('int64')

    # YouTube Categories
    def get_categories(youtube, wanted_categories):

        all_data = []
        
        request = youtube.videoCategories().list(part='snippet', id=','.join(wanted_categories))
        
        response = request.execute()
        
        for i in range(len(response['items'])):
            data = dict(category_id = response['items'][i]['id'],
                    category= response['items'][i]['snippet']['title'])
            all_data.append(data)

        return all_data
    
    data['category_id'] = data['category_id'].astype('str')
    category_ids = data['category_id'].unique()
    category_dict = get_categories(youtube, category_ids)
    category_df = pd.DataFrame(category_dict)
    data = pd.merge(data, category_df, on='category_id', how='left')

    # Extracting Duration
    data['duration'] = data['duration'].str.replace('PT', '')
    def format_duration(time_string):

        # store hours, minutes, seconds as integers
        H = 0
        M = 0
        S = 0

        # check if vid time contains hours, minutes and/or seconds
        if 'H' in time_string:
            H += int(time_string.split('H')[0])
        if 'M' in time_string:
            M += int(time_string.split('M')[0].split('H')[-1])
        if 'S' in time_string:
            S += int(time_string.split('S')[0].split('M')[-1].split('H')[-1])
        
        formatted_time = timedelta(hours=H, minutes=M, seconds=S)

        return formatted_time

    data['duration_formatted'] = data['duration'].apply(format_duration)

    # Object to Bool
    columns_to_bool = ['caption', 'licensed_content']

    for column in columns_to_bool:
        data[column] = data[column].astype('bool')

    # Creating No. of Tags Column
    data['no_of_tags'] = data['tags'].apply(lambda x: len(set(x)))

    # Creating Title Length Column
    data['title_length'] = data['title'].apply(len)

    # Creating Description Length Column
    data['description_length'] = data['description'].apply(len)

    # Dropping Columns
    columns_to_drop = ['category_id', 'duration', 'content_rating', 'default_language', 'favourite_count']
    data.drop(columns=columns_to_drop, inplace=True)

    return data


def day_gen(data):

    # converting published at
    data['published_at_formatted'] = data['published_at'].str.replace('Z','')
    data['published_at_formatted'] = data.published_at_formatted.apply(datetime.datetime.fromisoformat)

    # converting extraction date
    data['extraction_date_formatted'] = pd.to_datetime(data['extraction_date'], format='%Y-%m-%d %H:%M:%S')

    # creating Day column
    data['Day'] =  ((data['extraction_date_formatted'] - data['published_at_formatted']).dt.days) + 1

    data.drop(columns=['published_at', 'extraction_date'], inplace=True)

    return data


def merge_clean_function(running_df, new_df):
    # cleaning the data
    clean_new_df = clean(new_df)

    # generate day column
    day_clean_new_df = day_gen(clean_new_df)
    
    # concat with running df
    running_df = pd.concat([running_df, day_clean_new_df])
    running_df.reset_index(drop=True, inplace=True)

    return running_df

def save_data(dataframe):
    
    bucket = client.get_bucket(bucket_name)
    csv_string = dataframe.to_csv(index=False)
    blob = bucket.blob(f'{running_data_folder}running_youtube_video_data.csv')
    blob.upload_from_string(csv_string, content_type='text/csv')

if __name__ == "__main__":
    main()