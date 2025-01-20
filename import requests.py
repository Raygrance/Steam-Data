import requests

# Your Steam API key
API_KEY = "766F3C54C068E1A7C1468651EBD72634"

# Steam API Base URL
BASE_URL = "https://api.steampowered.com"

PLAYER_ID = 76561198306889297

def getAllAchievements(player_ID):
    games_list = getAllGames(player_ID)

    for game in games_list:
        
        print(f"\n\n--------------------------------------------------------------------------------\nAchievements for {game.get('name')}:")

        achievements_endpoint = f"{BASE_URL}/ISteamUserStats/GetPlayerAchievements/v1/"
        params = {
            "key": API_KEY,
            "steamid": player_ID, 
            "appid": game['appid'],
            "l": 'english'
        }
        response = requests.get(achievements_endpoint, params=params)

        if (response.status_code == 200):

            achievements = response.json().get('playerstats', {}).get('achievements', [])
            for achievement in achievements:
                print(f"- Achievement: {achievement.get('name', "null")}, Unlocked: {achievement.get('achieved')}, Unlock Date: {achievement.get('unlocktime')}")
        else:
            print(f"Error: Game has no Achievements")


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
        print(f"Num games = {response.json().get('response', {}).get('game_count')}")
        return response.json().get("response", {}).get("games", [])
    else:
        print(f"Error: {response.status_code} - {response.text}")

def main():
    getAllAchievements(PLAYER_ID)


if __name__ == "__main__":
    main()

    


