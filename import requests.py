import requests
from datetime import datetime
import csv

# Your Steam API key
API_KEY = "766F3C54C068E1A7C1468651EBD72634"

# Steam API Base URL
BASE_URL = "https://api.steampowered.com"

RAYGRANCE_ID = 76561198306889297

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
        
        elif response.status_code == 400:
            print(f"Error: {game.get('name')} has no achievements")
        else:
            print(f"Error: {response.status_code} - {response.text}")

    return output

################################################################################################################

def getAllGames(playerID):
    games_list_endpoint = f"{BASE_URL}/IPlayerService/GetOwnedGames/v1/"
    params = {
        "key": API_KEY,
        "steamid": playerID, 
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
        "steamids": playerID
    }
    response = requests.get(endpoint, params=params)
    if (response.status_code == 200):
        return response.json()['response']['players'][0].get('personaname', playerID)

################################################################################################################

def getInputPlayerID():
    
    while True:
        playerID = input("Enter Steam Player ID, type 'default' for example: ")
        if (playerID == 'default'):
            print(f"Using Raygrance PlayerID: {RAYGRANCE_ID}")
            return RAYGRANCE_ID
        elif ((not playerID.isdigit()) or (playerID == "")):
            print("Error, invalid ID entered")
        else:
            return playerID

################################################################################################################

def getVisibilityStatus(playerID):
    endpoint = f"{BASE_URL}/ISteamUser/GetPlayerSummaries/v2/"
    params = {
        "key": API_KEY,
        "steamid": playerID
    }
    response = requests.get(endpoint, params=params)
    
    if (response.status_code == 200):
        return response.json()['response']['players'][0].get('communityvisibilitystate', None) == 3
    else:
        return False
    
################################################################################################################

def getPublicFriends(playerID):
    publicFriends = []
    endpoint = f"{BASE_URL}/IsteamUser/GetFriendList/v1/"
    params = {
        "key": API_KEY,
        "steamid": playerID,
        "relationship": "all"
    }
    response = requests.get(endpoint, params=params)

    if (response.status_code == 200):
        for friend in response.json().get('friendslist', {}).get('friends', []):
            publicFriends.append(friend["steamid"])
    elif (response.status_code == 401):
        print("Error: Friends List is Private")
    else:
        print(f"Error: {response.status_code} - {response.text}")

    return publicFriends

################################################################################################################

def main():
    playerID = getInputPlayerID()

    print(getVisibilityStatus(playerID))

    # for friend in getPublicFriends(playerID):
    #     if (getVisibilityStatus(friend)):
    #         output = getAllAchievements(friend)
    #         with open(f"{getPlayerName(friend)}Achievements.csv", "w", errors='replace', newline="") as csvfile:
    #             writer = csv.writer(csvfile)
    #             writer.writerows(output)

################################################################################################################

if __name__ == "__main__":
    main()

