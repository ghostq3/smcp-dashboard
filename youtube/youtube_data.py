"""Third Party imports."""
import requests
import pandas as pd
from datetime import datetime, timedelta


# Define a datetime object for the current date and time
now = datetime.utcnow()

# Define a datetime object for 7 days ago
days_ago = now - timedelta(days=7)

# Format the datetime objects as ISO 8601 strings
now_str = now.strftime("%Y-%m-%dT%H:%M:%SZ")
days_ago_str = days_ago.strftime("%Y-%m-%dT%H:%M:%SZ")

import datetime


def get_video_data(api_key, search_query):
    """Get video data."""
    video_data = []
    now = datetime.datetime.utcnow()
    days_ago = now - datetime.timedelta(
        days=7
    )  # Get videos published within the last 7 days
    days_ago_str = days_ago.strftime("%Y-%m-%dT%H:%M:%SZ")

    for i in range(6):
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q=allintitle%3A{search_query}&type=video&maxResults=50&key={api_key}&publishedAfter={days_ago_str}"
        if i > 0:
            url += f"&pageToken={next_page_token}"

        response = requests.get(url)

        if response.status_code != 200:
            print(
                "Error: Failed to retrieve video search data. Response code:",
                response.status_code,
            )
            return []

        video_ids = [item["id"]["videoId"] for item in response.json()["items"]]
        stats_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={','.join(video_ids)}&key={api_key}"

        stats_response = requests.get(stats_url)
        if stats_response.status_code != 200:
            print(
                "Error: Failed to retrieve video statistics data. Response code:",
                stats_response.status_code,
            )
            return []

        stats_data = stats_response.json()
        try:
            for item in stats_data["items"]:
                channel_url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={item['snippet']['channelId']}&key={api_key}"
                channel_response = requests.get(channel_url)
                if channel_response.status_code != 200:
                    print(
                        "Error: Failed to retrieve channel data. Response code:",
                        channel_response.status_code,
                    )
                    continue

                video_id = item["id"]
                published_date = item["snippet"]["publishedAt"]
                title = item["snippet"]["title"]
                view_count = item["statistics"]["viewCount"]
                like_count = item["statistics"]["likeCount"]
                comment_count = item["statistics"]["commentCount"]
                channel_title = channel_response.json()["items"][0]["snippet"]["title"]
                subscriber_count = channel_response.json()["items"][0]["statistics"][
                    "subscriberCount"
                ]

                video_data.append(
                    [
                        video_id,
                        published_date,
                        title,
                        view_count,
                        like_count,
                        comment_count,
                        channel_title,
                        subscriber_count,
                    ]
                )
        except:
            pass

        if "nextPageToken" in response.json():
            next_page_token = response.json()["nextPageToken"]
        else:
            break

    return video_data


def convert_to_csv(game, data):
    """Convert data to CSV."""
    df = pd.DataFrame(
        data,
        columns=[
            "Video ID",
            "Published Date",
            "Title",
            "View Count",
            "Like Count",
            "Comment Count",
            "Channel Title",
            "Subscriber Count",
        ],
    )
    game_name = game.replace(" ", "_")
    df.to_csv(f"{game_name}.csv")


api_key = "AIzaSyBO5VBo-XQQD3R4fVY4CYJ8ExGtEy_jw9w"

game_list = [
    'Townstar Game',
    'Parallel Game',
    'Parallel TCG',
    'Axie Infinity',
    'Splinterlands',
    'Deadrop',
    'Illuvium',
    'GodsUnchained',
    'The Sandbox',
    'The Machines Arena',
    'Decentraland',
    'Other Side Meta',
    'Tribesters World',
    'Battle Bears',
    'Aurory Project',
    'zed_run',
    'Nine Chronicles',
    'Walken_io',
    'Blockchain Cutie',
    '0xSunflowerland',
    'Undeadblocks',
    'Dehero',
    'Panzerdogs',
    'Chain Guardians',
    'Cryptoblades',
    'play_evio',
    'Spider Tanks',
    'League Kingdoms',
    'Pixels Online'
]

for game in game_list:
    """Loop Though all of the games"""
    print(f"Searching for video of {game}")
    vid_data = get_video_data(api_key, game)
    convert_to_csv(game, vid_data)
