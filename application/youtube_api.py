from googleapiclient.discovery import build

api_key = 'AIzaSyC5KPqjgkghi5Q0JW8aXiMdahWIGyEB8Ek'

def get_yt_search_results(search_query):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(q=search_query, part='id, snippet', type='video', maxResults=10)
    result = request.execute()

    result_list = []

    for item in result['items']:
        id = 1
        title =  item['snippet']['title']
        yt_url = "https://www.youtube.com/watch?v="+item['id']['videoId']
        thumbnail_url = item['snippet']['thumbnails']['default']['url']

        item_dict = {
            "id": id,
            "name": title,
            "video_url": yt_url,
            "thumbnail_url": thumbnail_url
        }

        result_list.append(item_dict)

        id += 1
    

    return result_list