# test_checker
# Wed Sep 23 18:16:41 2026
# Jacob Birch

"""
This file will check if the italki API returns correctly
"""

# %% Initializing

import pytest
import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

DISCORD_WEBHOOK = os.getenv("webhook")

LANGUAGE = "Spanish"
API_URL = "https://support.italki.com/api/v2/help_center/en-us/articles/115001499873.json"

@pytest.fixture(scope='module')
def json_response():
    response = requests.get(
        API_URL, headers={"Accept": "application/json"}, timeout=15
    )
    return response


@pytest.fixture(scope='module')
def rows(json_response):
    soup = BeautifulSoup(json_response.json()["article"]["body"], "html.parser")
    return soup.find_all('tr')

def test_connection(json_response): # Make sure we are getting a connection first
    assert json_response.status_code == 200

def test_header_row(rows): # Make sure the headers are as expected
    header = [cell.get_text(strip=True) for cell in rows[0].find_all('td')]
    assert header == ['Language','Professional Teacher', 'Community Tutor']
    
    
def test_rows_are_three_cells(rows): # Make sure it's always Language, Profess, Community
    for row in rows:
        assert len(row.find_all('td')) == 3
        
        
def test_statuses_are_open_or_closed(rows): # Make sure they're formatted as Open & Closed
    expected_statuses = {'Open', 'Closed'}
    for row in rows[1:]:
        cells = [cell.get_text(strip=True) for cell in row.find_all('td')]
        assert cells[1] in expected_statuses, cells
        assert cells[2] in expected_statuses, cells
    
    
    
if __name__ == '__main__':
    pytest.main([__file__,'-vs'])