import requests
import time
from bs4 import BeautifulSoup

URL = "https://tacticalairwar.com/pilot.php?name=ACG_Wind"

label_aliases = {
    "Take-Offs": "Sorties",
    "Air Kills": "Aerial Victories",
    "Ground Kills": "Ground Targets Destroyed",
    "Total Flight Time": "Flight Time",
    "Combat Points":"CP"
}


def get_taw_stats():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(URL, headers=headers)
    if not response.ok:
        raise Exception(f"Failed to load page: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    stats = {}

    for row in soup.select("table tr"):
        cells = row.find_all("td")
        if len(cells) == 2:
            label = cells[0].text.strip()
            value = cells[1].text.strip()
            if label in ["Total Flight Time", "Take-Offs", "Air Kills","Ground Kills", "Deaths", "Captures", "Next Plane","Combat Points"]:
                stats[label] = value

        # Get all <p class="mb-0"> tags
        info_tags = soup.find_all("p", class_="mb-0")

        if len(info_tags) >= 2:
            stats["Squad"] = info_tags[0].get_text(strip=True)
            stats["Rank"] = info_tags[1].get_text(strip=True)

    return stats

# def write_stats_to_file(stats, filename="taw_stats.txt"):
#     with open(filename, "w") as f:
#         f.write(f"Tactical Air War Tour:     ")
#         # organize stats from stats.items() for use in output text
#         for k, v in stats.items():
#             f.write(f"{k}: {v}\n")

def write_stats_to_file(stats, filename="taw_stats.txt"):
    order = ["Air Kills","Ground Kills","Deaths","Captures","Take-Offs","Combat Points"]  # Add more if needed
    #ordered_items = [(k, stats[k]) for k in order if k in stats]
    items = [(label_aliases.get(k, k), stats[k]) for k in order if k in stats]

    midpoint = len(items) // 2
    with open(filename, "w") as f:
        f.write(f"Tactical Air War Tour - Squad: {stats.get('Squad','N/A')}   Rank: {stats.get('Rank','N/A')}  Flight Time: {stats.get('Total Flight Time','N/A')}\n")
        f.write("  ".join(f"{k}: {v}" for k, v in items[:midpoint]) + "  ")
        f.write("  ".join(f"{k}: {v}" for k, v in items[midpoint:]))

while True:
    if __name__ == "__main__":
        stats = get_taw_stats()
        write_stats_to_file(stats)
        print("Stats written to taw_stats.txt")
    time.sleep(3600)  # Wait 1 hour before fetching again