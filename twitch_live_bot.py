import requests
import json
import time

# Configuration
TWITCH_CHANNEL_NAME = 'pisitz'
TWITCH_CLIENT_ID = 'ew4p6gmzldwpnsgn6nvjdmf86hlgdq'
TWITCH_CLIENT_SECRET = 'ixei9rjbv5cjp4oqkrm2g84vwzjvhc'
DISCORD_WEBHOOK_URL = 'https://canary.discord.com/api/webhooks/1231315076099604511/6JGur6nD6TCE7_LfY6FWfZ3ARLPQKfn-36HVrfAq_K92ODsMy6eRoRtAQXBJywB0flEr'
CHECK_INTERVAL = 60  # Check every 60 seconds

# Get Twitch OAuth Token
def get_twitch_oauth_token(client_id, client_secret):
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, params=params)
    return response.json().get('access_token')

# Check if the channel is live
def is_channel_live(channel_name, client_id, oauth_token):
    url = f'https://api.twitch.tv/helix/streams?user_login={channel_name}'
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {oauth_token}'
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return len(data['data']) > 0

# Send notification to Discord
def send_discord_notification(webhook_url, message):
    data = {
        'content': message
    }
    requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})

def main():
    oauth_token = get_twitch_oauth_token(TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET)
    notified = False

    while True:
        if is_channel_live(TWITCH_CHANNEL_NAME, TWITCH_CLIENT_ID, oauth_token):
            if not notified:
                send_discord_notification(DISCORD_WEBHOOK_URL, f"{TWITCH_CHANNEL_NAME} is now live on Twitch!")
                notified = True
        else:
            notified = False

        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    main()
