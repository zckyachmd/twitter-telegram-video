######################################
#                                    #
#         Twitter Video Grabber      #
#                                    #
######################################

# Project: Twitter Video Grabber
# Description: A Python script that automates the process of grabbing videos from Twitter and sending them to Telegram channel.
# Author: Zacky Achmad (@zckyachmd)
# Date: 2023-04-25
# Version: 1.0

import asyncio
import tweepy
import telegram
import time
import argparse
import os
import config

# Parsing argumen
parser = argparse.ArgumentParser(description='Send video from Twitter to Telegram')
parser.add_argument('--reset', action='store_true', help='Reset config.log_tweet file')
args = parser.parse_args()

# Check if reset argument is passed
if args.reset:
    # Reset file config.log_tweet
    with open(config.log_tweet, 'w') as file:
        file.write('')  # Write empty string to reset file

# Check if config.log_tweet file exists
if not os.path.exists(config.log_tweet):
    with open(config.log_tweet, 'w'):
        pass

# Read tweet ID that has been sent from file
with open(config.log_tweet, 'r') as file:
    sent_tweet_ids = set(int(tweet_id.strip()) for tweet_id in file.readlines())

# Auth to Twitter
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)

# Create API Twitter object
api = tweepy.API(auth)

# Get tweets from target
if sent_tweet_ids:
    tweets = api.user_timeline(screen_name=config.twitter_target, count=200, include_rts=True, tweet_mode="extended", since_id=max(sent_tweet_ids))
else:
    tweets = api.user_timeline(screen_name=config.twitter_target, count=200, include_rts=True, tweet_mode="extended")

# Auth to Telegram
bot = telegram.Bot(token=config.telegram_bot_token)

# Async function to send video to Telegram channel
async def send_video_to_telegram(chat_id, video_url, idx):
    try:
        await bot.send_video(chat_id=chat_id, video=video_url)
        return True
    except telegram.error.BadRequest as e:
        print(f'Error processing data {idx}: {e} - Wrong file identifier/http url specified')
        return False
    except telegram.error.RetryAfter as e:
        print(f'Error processing data {idx}: {e} - Flood control exceeded. Retry after {e.retry_after} seconds')
        time.sleep(e.retry_after)  # Wait for given seconds before retrying
        return False
    except telegram.error.TimedOut as e:
        print(f'Error processing data {idx}: {e} - Timed out')
        return False
    except Exception as ex:
        print(f'Error processing data {idx}: {ex}')
        return False

# Async main function to send video to Telegram channel
async def main():
    sent_tweet_ids = set()
    successful = 0
    failed = 0

    # Print total tweets
    print(f'Total Tweets: {len(tweets)}')

    # Get tweets from target
    for idx, tweet in enumerate(tweets, start=1):
      if "extended_entities" in tweet._json:
          if "media" in tweet._json["extended_entities"]:
              if tweet._json["extended_entities"]["media"][0]["type"] == "video":
                  # Get video URL
                  video_url = tweet._json["extended_entities"]["media"][0]["video_info"]["variants"][0]["url"]

                  if tweet.id not in sent_tweet_ids:
                      try:
                          # Send video to Telegram channel with timeout
                          if await send_video_to_telegram(chat_id=config.chat_id, video_url=video_url, idx=idx):
                              successful += 1

                              # Save tweet ID to file after successfully sent
                              with open(config.log_tweet, 'a') as file:
                                  file.write(f'{tweet.id}\n')
                          else:
                              failed += 1 # Increment failed count if sending video failed
                      except Exception as ex:
                          print(f'Error processing data {idx}: {ex}')
                          failed += 1 # Increment failed count if an exception occurred

    # Print  successful, and failed count after sending all videos
    print(f'Total Successful: {successful}')
    print(f'Total Failed: {failed}')

# Run event loop async
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
