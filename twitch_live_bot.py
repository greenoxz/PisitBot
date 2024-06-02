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

# Check if the channel is live and get stream data
def get_stream_data(channel_name, client_id, oauth_token):
    url = f'https://api.twitch.tv/helix/streams?user_login={channel_name}'
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {oauth_token}'
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    if len(data['data']) > 0:
        return data['data'][0]  # Return stream data
    return None

# Send notification to Discord
def send_discord_notification(webhook_url, channel_name, stream_data):
    channel_url = f"https://www.twitch.tv/{channel_name}"
    stream_preview_url = stream_data['thumbnail_url'].replace('{width}', '1280').replace('{height}', '720')
    profile_image_url = "https://static-cdn.jtvnw.net/jtv_user_pictures/28471127-7b48-4f6c-a3d2-d459d2f0419d-profile_image-70x70.png"  # Example profile image URL, replace as needed
    created_at = stream_data['started_at']
    game_name = stream_data['game_name']

    embed_data = {
        "content": f"{channel_name} มาแล้ว @everyone",
        "embeds": [{
            "title": channel_url,
            "url": channel_url,
            "color": 6570404,
            "footer": {
                "text": created_at
            },
            "image": {
                "url": stream_preview_url
            },
            "author": {
                "name": f"{channel_name} มาแล้ว!"
            },
            "thumbnail": {
                "url": profile_image_url
            },
            "fields": [
                {
                    "name": "Playing",
                    "value": game_name,
                    "inline": true
                },
                {
                    "name": "Started at (streamer timezone)",
                    "value": created_at,
                    "inline": true
                }
            ]
        }]
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(webhook_url, data=json.dumps(embed_data), headers=headers)

def main():
    oauth_token = get_twitch_oauth_token(TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET)
    notified = False

    while True:
        stream_data = get_stream_data(TWITCH_CHANNEL_NAME, TWITCH_CLIENT_ID, oauth_token)
        if stream_data:
            if not notified:
                send_discord_notification(DISCORD_WEBHOOK_URL, TWITCH_CHANNEL_NAME, stream_data)
                notified = True
        else:
            notified = False

        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    main()
