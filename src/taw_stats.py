import requests
from bs4 import BeautifulSoup

URL = "https://tacticalairwar.com/pilot.php?name=ACG_Wind"

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

    return stats

def write_stats_to_file(stats, filename="taw_stats.txt"):
    with open(filename, "w") as f:
        f.write(f"Tactical Air War Tour:     ")
        # organize stats from stats.items() for use in output text
        for k, v in stats.items():
            f.write(f"{k}: {v}\n")

if __name__ == "__main__":
    stats = get_taw_stats()
    write_stats_to_file(stats)
    print("Stats written to taw_stats.txt")
