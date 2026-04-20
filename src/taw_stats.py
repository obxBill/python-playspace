import requests
import time
from bs4 import BeautifulSoup

BASE_URL = "https://tacticalairwar.com/pilot.php"
PILOT_NAME = "ACG_Wind"

LABEL_ALIASES = {
    "Air Kill Streak": "Aerial Victories",
    "Ground Kill Streak": "Ground Targets Destroyed",
    "Next Plane": "Next Plane",
    "Flight Time": "Latest Sortie",
    "Combat Points": "CP",
    "Mission": "Mission",
    "Result": "Status",
    "Aircraft Type": "Type"
}

STAT_ORDER = ["Mission", "Aircraft Type", "Result", "Air Kill Streak",
              "Ground Kill Streak", "Combat Points", "Next Plane"]


def get_taw_stats(pilot=PILOT_NAME):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(BASE_URL, params={"name": pilot}, headers=headers)
    if not response.ok:
        raise Exception(f"Failed to load page: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    stats = {}

    for row in soup.select("table tr"):
        cells = row.find_all("td")
        if len(cells) == 2:
            label = cells[0].text.strip()
            value = cells[1].text.strip()
            if label in STAT_ORDER + ["Flight Time"]:
                stats[label] = value

    info_tags = soup.find_all("p", class_="mb-0")
    if len(info_tags) >= 2:
        stats["Squad"] = info_tags[0].get_text(strip=True)
        stats["Rank"] = info_tags[1].get_text(strip=True)

    return stats


def write_stats_to_file(stats, filename="taw_stats.txt"):
    items = [(LABEL_ALIASES.get(k, k), stats[k]) for k in STAT_ORDER if k in stats]
    midpoint = len(items) // 2

    with open(filename, "w") as f:
        f.write(f"{stats.get('Squad', 'N/A')}  {stats.get('Rank', 'N/A')}    "
                f"Latest Sortie: {stats.get('Flight Time', 'N/A')}\n")
        f.write("  ".join(f"{k}: {v}" for k, v in items[:midpoint]) + "  ")
        f.write("  ".join(f"{k}: {v}" for k, v in items[midpoint:]))


if __name__ == "__main__":
    while True:
        try:
            stats = get_taw_stats()
            write_stats_to_file(stats)
            print("Stats written to taw_stats.txt")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(3600)