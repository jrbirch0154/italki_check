# check_italki_api.py
# Wed Sep 23 17:59:49 2026
# Jacob Birch

"""
Checks iTalki directly through the API. No playwright or BeautifulSoup required!
"""

# %% Initializing

import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

DISCORD_WEBHOOK = os.getenv("webhook")
if not DISCORD_WEBHOOK:
    raise SystemExit("Missing webhook in .env")

LANGUAGE = "Spanish"
API_URL = "https://support.italki.com/api/v2/help_center/en-us/articles/115001499873.json"
ARTICLE_URL = "https://support.italki.com/hc/en-us/articles/115001499873"

# %% Get statuses


def get_status(language):
    """
    Returns (professional status, community status)
    """
    response = requests.get(
        API_URL, headers={"Accept": "application/json"}, timeout=15
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.json()["article"]["body"], "html.parser")
    rows = soup.find_all('tr')

    for row in rows:
        cells = row.find_all("td")
        # print([c.get_text(strip=True) for c in cells])

        if len(cells) >= 3 and cells[0].get_text(strip=True) == language:
            return cells[1].get_text(strip=True), cells[2].get_text(strip=True)
        
        

    return "Open (not listed)", "Open (not listed)"


prof, com = get_status(LANGUAGE)
print(f"Professional Teacher: {prof}\nCommunity Tutor: {com}")

if com.startswith('Open'):
    requests.post(
        DISCORD_WEBHOOK,
        json={
            "content": (
                "Spanish is open on iTalki!\n"
                f"Professional: {prof}\n"
                f"Community: {com}\n{API_URL}\n{ARTICLE_URL}"
            )
        },
        timeout=15,
    )