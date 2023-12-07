from googleapiclient.discovery import build
import pandas as pd
import pickle

def main():

    api_key = 'AIzaSyBAobEQD70yA3gEWGjeZxGfyvvlwvMDsr8'

    youtube = build('youtube', 'v3', developerKey=api_key)


# list of playlist ids
def chosen_playlist_ids():
    file_path = r'C:\Users\lawre\Documents\GitHub\YouTube-Analytics\chosen_playlist_ids.pkl'

    with open(file_path, 'rb') as file:
        playlist_ids = pickle.load(file)
    
    return playlist_ids

# rename to day 0 / legacy data
def get_base_list():
    file_path = r'C:\Users\lawre\Documents\GitHub\YouTube-Analytics\base_video_id_list.pkl'

    with open(file_path, 'rb') as file:
        base_video_id_list = pickle.load(file)

    return base_video_id_list

# running video collection of day 1 - day7+ video ids list
def get_grab_list():
    file_path = r'C:\Users\lawre\Documents\GitHub\YouTube-Analytics\grab_list.pkl'

    with open(file_path, 'rb') as file:
        grab_list = pickle.load(file)

    return grab_list


# function to get video ids from youtube, which generates new list everyday
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
    # 
    all_data_df = pd.DataFrame(all_data)

    retrived_video_ids = all_data_df['video_id']

    return retrived_video_ids


# identifies post day 0 videos
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


# 
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
    with open('grab_list.pkl', 'wb') as file:
        pickle.dump(grab_list, file)

    return grab_list


def get_video_stats(youtube, list_of_video_ids):

    all_data = []

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
                        tags = video['snippet'].get('tags', []), # was issue here as not all videos had tags, .get() might generally offer better protection
                        category_id = video['snippet'].get('categoryId'),
                        duration = video['contentDetails'].get('duration'),
                        caption = video['contentDetails'].get('caption'),
                        licensed_content = video['contentDetails'].get('licensedContent'),
                        default_language = video['snippet'].get('defaultLanguage'),
                        content_rating = video['contentDetails'].get('contentRating'),
                        view_count = video['statistics'].get('viewCount'),
                        like_count = video['statistics'].get('likeCount'), # issue 
                        favourite_count = video['statistics'].get('favoriteCount'),
                        comment_count = video['statistics'].get('commentCount'))

            all_data.append(data)

    all_data_df = pd.DataFrame(all_data)

    return all_data_df


## saving daily collection dataframes
def save_day_1_df(df):
    with open('day_1_df.pkl', 'wb') as file:
        pickle.dump(df, file)
def save_day_2_df(df):
    with open('day_2_df.pkl', 'wb') as file:
        pickle.dump(df, file)
def save_day_3_df(df):
    with open('day_3_df.pkl', 'wb') as file:
        pickle.dump(df, file)
def save_day_4_df(df):
    with open('day_4_df.pkl', 'wb') as file:
        pickle.dump(df, file)
def save_day_5_df(df):
    with open('day_5_df.pkl', 'wb') as file:
        pickle.dump(df, file)
def save_day_6_df(df):
    with open('day_6_df.pkl', 'wb') as file:
        pickle.dump(df, file)
def save_day_7_df(df):
    with open('day_7_df.pkl', 'wb') as file:
        pickle.dump(df, file)

## loading daily collection dataframes
def get_day_1_df():
    file_path = r'C:\Users\lawre\Documents\GitHub\YouTube-Analytics\day_1_df.pkl'

    with open(file_path, 'rb') as file:
        day_1_df = pickle.load(file)

    return day_1_df
def get_day_2_df():
    file_path = r'C:\Users\lawre\Documents\GitHub\YouTube-Analytics\day_2_df.pkl'

    with open(file_path, 'rb') as file:
        day_2_df = pickle.load(file)

    return day_2_df
def get_day_3_df():
    file_path = r'C:\Users\lawre\Documents\GitHub\YouTube-Analytics\day_3_df.pkl'

    with open(file_path, 'rb') as file:
        day_3_df = pickle.load(file)

    return day_3_df
def get_day_4_df():
    file_path = r'C:\Users\lawre\Documents\GitHub\YouTube-Analytics\day_4_df.pkl'

    with open(file_path, 'rb') as file:
        day_4_df = pickle.load(file)

    return day_4_df
def get_day_5_df():
    file_path = r'C:\Users\lawre\Documents\GitHub\YouTube-Analytics\day_5_df.pkl'

    with open(file_path, 'rb') as file:
        day_5_df = pickle.load(file)

    return day_5_df
def get_day_6_df():
    file_path = r'C:\Users\lawre\Documents\GitHub\YouTube-Analytics\day_6_df.pkl'

    with open(file_path, 'rb') as file:
        day_6_df = pickle.load(file)

    return day_6_df
def get_day_7_df():
    file_path = r'C:\Users\lawre\Documents\GitHub\YouTube-Analytics\day_7_df.pkl'

    with open(file_path, 'rb') as file:
        day_7_df = pickle.load(file)

    return day_7_df


def sorter(new_day_df):

    # Calling functions for dataframes
    day_1_df = get_day_1_df()
    day_2_df = get_day_2_df()
    day_3_df = get_day_3_df()
    day_4_df = get_day_4_df()
    day_5_df = get_day_5_df()
    day_6_df = get_day_6_df()
    day_7_df = get_day_7_df()


    # Iterating and appending new data
    for index, row in new_day_df.iterrows():

        if row['video_id'] not in list(day_1_df['video_id']):
            day_1_df = pd.concat([day_1_df, row.to_frame().transpose()], ignore_index=True)
        elif row['video_id'] not in list(day_2_df['video_id']):
            day_2_df = pd.concat([day_2_df, row.to_frame().transpose()], ignore_index=True)
        elif row['video_id'] not in list(day_3_df['video_id']):
            day_3_df = pd.concat([day_3_df, row.to_frame().transpose()], ignore_index=True)
        elif row['video_id'] not in list(day_4_df['video_id']):
            day_4_df = pd.concat([day_4_df, row.to_frame().transpose()], ignore_index=True)
        elif row['video_id'] not in list(day_5_df['video_id']):
            day_5_df = pd.concat([day_5_df, row.to_frame().transpose()], ignore_index=True)
        elif row['video_id'] not in list(day_6_df['video_id']):
            day_6_df = pd.concat([day_6_df, row.to_frame().transpose()], ignore_index=True)
        elif row['video_id'] not in list(day_7_df['video_id']):
            day_7_df = pd.concat([day_7_df, row.to_frame().transpose()], ignore_index=True)
        else:
            continue
        

    # Saving new dataframes
    save_day_1_df(day_1_df)
    save_day_2_df(day_2_df)
    save_day_3_df(day_3_df)
    save_day_4_df(day_4_df)
    save_day_5_df(day_5_df)
    save_day_6_df(day_6_df)
    save_day_7_df(day_7_df)


if __name__ == "__main__":
    main()