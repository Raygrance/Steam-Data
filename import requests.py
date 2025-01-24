import requests
from datetime import datetime
import csv

# Your Steam API key
API_KEY = "766F3C54C068E1A7C1468651EBD72634"

# Steam API Base URL
BASE_URL = "https://api.steampowered.com"

PLAYER_ID = 765611983068892967
# Raygrance player ID 765611983068892967

################################################################################################################

def getAllAchievements(player_ID):
    games_list = getAllGames(player_ID)
    output = [["game", "achievement", "description", "achieved", "unlocktime"]]

    for game in games_list:

        # gets list of all achievements for all games owned by player
        achievements_endpoint = f"{BASE_URL}/ISteamUserStats/GetPlayerAchievements/v1/"
        params = {
            "key": API_KEY,
            "steamid": player_ID, 
            "appid": game['appid'],
            "l": 'english'
        }
        response = requests.get(achievements_endpoint, params=params)

        # appends data to list
        if (response.status_code == 200):
            achievements = response.json().get('playerstats', {}).get('achievements', [])
            # iteratres through achievements
            for achievement in achievements:
                entry = [
                    f"{game.get('name')}",  # Assuming this key will always exist, you might want to check for None as well if needed
                    f"{achievement.get('name')}",
                    f"{achievement.get('description') if achievement.get('description') else 'no description available'}",
                    f"{achievement.get('achieved') == 1}",
                    f"{datetime.fromtimestamp(achievement.get('unlocktime')) if achievement.get('achieved') else 'null'}"
                ]

                output.append(entry)

        else:
            print(f"Error: Game has no Achievements")
    return output

################################################################################################################

def getAllGames(playerID):
    games_list_endpoint = f"{BASE_URL}/IPlayerService/GetOwnedGames/v1/"
    params = {
        "key": API_KEY,
        "steamid": PLAYER_ID, 
        "include_played_free_games": True,
        "include_appinfo": True
    }
    response = requests.get(games_list_endpoint, params=params)

    if (response.status_code == 200):
        return response.json().get("response", {}).get("games", [])
    else:
        print(f"Error: {response.status_code} - {response.text}")

################################################################################################################

def getPlayerName(playerID):
    endpoint = f"{BASE_URL}/ISteamUser/GetPlayerSummaries/v2/"
    params = {
        "key": API_KEY,
        "steamids": PLAYER_ID
    }
    response = requests.get(endpoint, params=params)
    if (response.status_code == 200):

        return response.json()['response']['players'][0].get('personaname', PLAYER_ID)

################################################################################################################

def main():
    output = getAllAchievements(PLAYER_ID)

    with open(f"{getPlayerName(PLAYER_ID)}Achievements.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(output)

################################################################################################################

if __name__ == "__main__":
    main()