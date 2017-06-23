from chalice import Chalice
from urllib import urlopen
import json
import boto3

app = Chalice(app_name='coding-challenge')
s3 = boto3.client('s3')

@app.route('/')
def index():
    return """Hello! You have reached Jeff's Rad Publishing Service!
Your IP address is {0}!
Here's a rad 200 OK Status for your troubles!\n""".format(app.current_request.context.get('identity').get('sourceIp'))

@app.route('/artist/{artist}')
def artist_info(artist):
    tags_url = "http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={0}&api_key=4d82588e27228e7938bacde4bee73422&format=json".format(artist)
    tracks_url = "http://ws.audioscrobbler.com/2.0/?method=artist.getTopTracks&artist={0}&api_key=4d82588e27228e7938bacde4bee73422&format=json".format(artist)
    info = json.load(urlopen(tags_url))
    tags = info["artist"]["tags"]["tag"]
    tracks = json.load(urlopen(tracks_url))["toptracks"]["track"]
    return """Here's a little info about {0}. This artist has been tagged as {1}, {2}, {3}, {4}, and {5}.
Their most popular songs are:
{6}
{7}
{8}
{9}
{10}\n""".format(info["artist"]["name"], tags[0]["name"], tags[1]["name"], tags[2]["name"], tags[3]["name"], tags[4]["name"], \
tracks[0]["name"], tracks[1]["name"], tracks[2]["name"], tracks[3]["name"], tracks[4]["name"])

@app.route('/image')
def image_publish():
    s3.put_object(
        Body="<html><img src={0}></html>".format(app.current_request.query_params.get('image-file')),
        Bucket="coding-challenge-dev",
        ContentType="text/html",
        Key="image.html"
    )
    s3.put_object_acl(ACL='public-read', Bucket='coding-challenge-dev', Key='image.html')
    return "See your image here: https://s3.amazonaws.com/coding-challenge-dev/image.html\n"
