import tweepy
import random
import os
import json
import dropbox

# 環境変数からTwitter API認証情報を取得
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
dropbox_token = os.getenv('DROPBOX_TOKEN')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Dropboxクライアントを設定
dbx = dropbox.Dropbox(dropbox_token)

# 投稿内容の読み込み
with open('posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

def get_random_post():
    return random.choice(posts)

def download_video_from_dropbox(dropbox_path, local_path):
    with open(local_path, "wb") as f:
        metadata, res = dbx.files_download(path=dropbox_path)
        f.write(res.content)

def post_to_twitter():
    post = get_random_post()
    local_video_path = "/tmp/temp_video.mp4"

    # Dropboxからビデオをダウンロード
    download_video_from_dropbox(post['video1'], local_video_path)

    # 最初の投稿
    media = api.media_upload(local_video_path)
    status1 = api.update_status(status=post['text1'], media_ids=[media.media_id_string])

    # ツリー投稿
    api.update_status(status=post['text2'] + " " + post['link2'], in_reply_to_status_id=status1.id, auto_populate_reply_metadata=True)

if __name__ == "__main__":
    post_to_twitter()

