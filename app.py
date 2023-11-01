from flask import Flask, redirect, render_template, jsonify, request
from youtube import updatechannelvideos, find_videos, video_details

app = Flask(__name__)

VIDEOS_LIST = []


def time_format(value):
    hour = int(value / (60 * 60 * 1000))
    value -= hour * (60 * 60 * 1000)
    minutes = int(value / 60000)
    value -= minutes * 60000
    seconds = int(value / 1000)
    micro = value % 1000
    return f'{"{:02d}".format(hour)}:{"{:02d}".format(minutes)}:{"{:02d}".format(seconds)}.{"{:03d}".format(micro)}'


def count(videos):
    answer = 0
    for key in videos:
        answer += len(videos[key])
    return answer


app.jinja_env.filters["time_format"] = time_format
app.jinja_env.filters["count"] = count


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def gethello():
    return render_template("index.html", page=None, videos=None, total=None)


@app.route("/", methods=["POST"])
def posthello():
    query = request.form.get("query")
    page = request.form.get("page")
    if not page:
        page = 1
    VIDEOS_LIST = find_videos(query)
    total_videos = len(VIDEOS_LIST)
    total = 0
    for video in VIDEOS_LIST:
        for word in VIDEOS_LIST[video]:
            total += len(VIDEOS_LIST[video][word])
    print(VIDEOS_LIST)
    return render_template(
        "index.html",
        page=page,
        videos=VIDEOS_LIST,
        total_videos=total_videos,
        total=total,
    )


@app.route("/add/channel", methods=["GET"])
def insert_channel():
    return render_template("channel.html")


@app.route("/add/channel", methods=["POST"])
def channel():
    channel_url = request.form.get("url")
    updatechannelvideos(channel_url)
    return redirect("/add/channel")


@app.route("/details", methods=["POST"])
def details():
    video = request.form.get("video")
    details = video_details(video)
    dict_details = {}
    dict_details["channel"] = details.channel
    dict_details["upload"] = details.uploaddate
    dict_details["duration"] = details.duration
    dict_details["views"] = details.views
    return jsonify(dict_details)


@app.route("/more", methods=["GET"])
def more():
    return render_template("more.html")
