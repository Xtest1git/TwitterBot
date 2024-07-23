import tweepy
import os
import random
import json

# 環境変数からTwitter API認証情報を取得
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# 投稿内容の読み込み
with open('posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

def get_random_post():
    return random.choice(posts)

def post_to_twitter():
    post = get_random_post()
    video_path = post['video1']

    # メディアをアップロード
    try:
        media = api.media_upload(video_path, media_category='tweet_video')
        print("Media uploaded:", media.media_id_string)
    except tweepy.TweepError as e:
        print("Error uploading media:", e)
        return

    # 最初のツイートを投稿
    try:
        status1 = api.update_status(status=post['text1'], media_ids=[media.media_id_string])
        print("First tweet posted:", status1.id)
    except tweepy.TweepError as e:
        print("Error posting first tweet:", e)
        return

    # 返信ツイートを投稿
    try:
        api.update_status(status=post['text2'] + " " + post['link2'], in_reply_to_status_id=status1.id, auto_populate_reply_metadata=True)
        print("Reply tweet posted.")
    except tweepy.TweepError as e:
        print("Error posting reply tweet:", e)

if __name__ == "__main__":
    post_to_twitter()
