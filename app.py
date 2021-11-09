from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")

@app.route("/search")
def search_page():
    api_key = 'AIzaSyC5KPqjgkghi5Q0JW8aXiMdahWIGyEB8Ek'

    from googleapiclient.discovery import build

    youtube = build('youtube', 'v3', developerKey=api_key)
    search_query="Spiritbox circle with me" #ToDo
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
            "title": title,
            "video_url": yt_url,
            "thumbnail_url": thumbnail_url
        }

        result_list.append(item_dict)

        id += 1
    

    return render_template("search.html", items=result_list)
