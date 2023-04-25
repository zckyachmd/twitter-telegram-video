# Twitter Telegram Video

Twitter Telegram Video is a Python script that automates grabbing videos from a Twitter account and sending them to a Telegram channel. This script is designed to run as a standalone bot that can be scheduled to run periodically, allowing you to automatically share videos from a Twitter account to your Telegram channel.

## Prerequisites

Before using Twitter Telegram Video, you will need the following:

- Twitter API keys and access tokens. You can obtain these by creating a Twitter Developer Account and creating a new Twitter App. Make sure to note down the consumer key, consumer secret, access token, and access token secret.

- Telegram API bot token. You can obtain this by creating a new bot on Telegram using the BotFather bot. Make sure to note down the bot token.

- Read and Write permissions for the Telegram bot. The bot needs to have read and write permissions in order to send videos to the Telegram channel.

## Usage

1. Clone this repository to your local machine or server.

2. Install the required dependencies by running the following command:

```bash
pip install -r requirements.txt
```

3. Create a file named api_keys.py in the root directory of the project, and define the following variables with your Twitter and Telegram API credentials:

```bash
# Twitter API keys and access tokens
consumer_key = "your_consumer_key"
consumer_secret = "your_consumer_secret"
access_token = "your_access_token"
access_token_secret = "your_access_token_secret"
twitter_target = 'twitter_target'

# Telegram bot token
telegram_bot_token = "your_telegram_bot_token"
chat_id = "telegram_channel_id"
```

4. Run the script using Python, for example:

```bash
python twitter_telegram_video.py
```

5. The script will start grabbing videos from the Twitter account and sending them to the Telegram channel as configured. The videos will be sent as files to the Telegram channel, and the captions of the videos will be used as the captions for the Telegram messages.

## Author

[Zacky Achmad](https://twitter.com/zckyachmd) - [@zckyachmd](https://twitter.com/zckyachmd)

## License

This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) License.
