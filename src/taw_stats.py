import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

BASE_URL = "https://tacticalairwar.com/pilot.php"
PILOT_NAME = "ACG_Wind"

LABEL_ALIASES = {
    "Air Kill Streak": "Air Kill Streak",
    "Ground Kill Streak": "Ground Kill Streak",
    "Next Plane": "Next Plane",
    "Combat Points": "CP",
    "Mission": "Mission",
    "Result": "Result",
}

STAT_ORDER = ["Air Kill Streak", "Ground Kill Streak", "Combat Points", "Next Plane"]


def get_taw_stats(pilot=PILOT_NAME):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"{BASE_URL}?name={pilot}")
        page.wait_for_selector("table tr")
        soup = BeautifulSoup(page.content(), "html.parser")
        browser.close()

    stats = {}
    seen = set()

    for row in soup.select("table tr"):
        cells = row.find_all("td")
        if len(cells) == 2:
            label = cells[0].text.strip()
            value = cells[1].text.strip()
            if label in STAT_ORDER and label not in seen:
                stats[label] = value
                seen.add(label)

    # Rank
    info_tags = soup.find_all("p", class_="mb-0")
    if len(info_tags) >= 1:
        stats["Rank"] = info_tags[0].get_text(strip=True)

    # Latest sortie Mission, Result, Airframe
    sortie_table = soup.find_all("table", class_="mb-0")
    if sortie_table:
        tbody = sortie_table[0].find("tbody")
        if tbody:
            first_row = tbody.find("tr")
            if first_row:
                cells = first_row.find_all("td")
                if len(cells) >= 7:
                    stats["Mission"] = cells[1].text.strip()
                    stats["Result"] = cells[2].get_text(strip=True)
                    stats["Airframe"] = cells[6].text.strip()

    return stats


def write_stats_to_file(stats, filename="taw_stats.txt"):
    items = [(LABEL_ALIASES.get(k, k), stats[k]) for k in STAT_ORDER if k in stats]
    midpoint = len(items) // 2

    with open(filename, "w") as f:
        f.write(f"Tactical Air War      Current Rank: {stats.get('Rank', 'N/A')}  "
                f"Latest Sortie: {stats.get('Mission', 'N/A')}/{stats.get('Airframe', 'N/A')}/{stats.get('Result', 'N/A')}\n")
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
