import requests
import time
from bs4 import BeautifulSoup

pilot_url = "https://combatbox.net/en/pilot/7110/ACG_Wind/"
output_file = "combatbox_stats.txt"

while True:
    response = requests.get(pilot_url)
    soup = BeautifulSoup(response.text, "lxml")

    stats = {}

    # Find pilot summary cards
    cards = soup.select(".profile_main_stats .item")
    cards2 = soup.select(".player_detailed")
    cards3 = soup.select(".center_block .item")
    cards4 = soup.select(".nav_tour_select")

    for card in cards2:
        title = card.select_one(".title")
        if title and "Detailed sorties results" in title.text:
            rows = card.select(".item")
            for row in rows:
                label = row.select_one("div.name").text.strip()
                value = row.select_one("div.num").text.strip()
                stats[label] = value
        
    for card in cards:
        label = card.select_one("div.text").text.strip()
        value = card.select_one("div.num").text.strip()
        stats[label] = value
    
    for card in cards3:
        label = card.select_one("div.text").text.strip()
        value = card.select_one("div.num").text.strip()
        stats[label] = value

    for card in cards4:
        label = "Tour"
        value = card.select_one("div.nav_tour_selected").text.strip()
        stats[label] = value        

    # Write stats to file for OBS
    with open(output_file, "w") as f:
        f.write(f"CombatBox Tour: {stats.get('Tour', 'N/A')}     ")
        f.write(f"Pilot Rating (Fighter) {stats.get('Position Fighter Rating', 'N/A')}\n")
        f.write(f"Aerial Victories: {stats.get('Aerial victories', 'N/A')}  ")
        f.write(f"Ground Targets Destroyed: {stats.get('Destroyed on Ground', 'N/A')}  ")
        f.write(f"Kill/Death Ratio: {stats.get('K/D - Kills per Death', 'N/A')}  ")
        f.write(f"Sorties: {stats.get('Sorties', 'N/A')}  ")
        f.write(f"Flight Time: {stats.get('Flight Time', 'N/A')}  ")

    print(f"Stats written to {output_file}")
    time.sleep(3600)  # Wait 1 hour before fetching again