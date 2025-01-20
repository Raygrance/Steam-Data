from datetime import datetime
import requests

# Your Steam API key
API_KEY = "766F3C54C068E1A7C1468651EBD72634"

# Steam API Base URL
BASE_URL = "https://api.steampowered.com"

# Function to get Steam user's summary
def get_player_summary(steam_id):
    endpoint = f"{BASE_URL}/ISteamUser/GetPlayerSummaries/v2/"
    params = {
        "key": API_KEY,
        "steamids": steam_id,  # Single or comma-separated Steam IDs
    }

    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["response"]["players"][0] if data["response"]["players"] else None
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Function to get a list of owned games
def get_owned_games(steam_id):
    endpoint = f"{BASE_URL}/IPlayerService/GetOwnedGames/v1/"
    params = {
        "key": API_KEY,
        "steamid": steam_id,
        "include_appinfo": True,  # Include game details
        "include_played_free_games": True,
    }

    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["response"].get("games", [])
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Example usage
if __name__ == "__main__":
    STEAM_ID = "76561198306889297"  # Replace with a valid Steam ID

    # Get player summary
    player = get_player_summary(STEAM_ID)
    if player:
        print("Player Summary:")
        print(f"Name: {player.get('personaname')}")
        print(f"Profile URL: {player.get('profileurl')}")
        print(f"Avatar: {player.get('avatar')}")
        print(f"Last Log Off: {datetime.utcfromtimestamp(player.get('lastlogoff')).strftime('%Y-%m-%d %H:%M:%S')}")

    # Get owned games
    games = get_owned_games(STEAM_ID)
    if games:
        print("\nOwned Games:")
        for game in games:  # Display the first 10 games
            print(f"- {game['name']} ({game['playtime_forever']} mins played)")
