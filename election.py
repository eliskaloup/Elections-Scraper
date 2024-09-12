import sys
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

def response_server(url: str):
    """Fetches and parses the main URL to get bs4 object."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return bs(response.text, "html.parser")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        sys.exit(1)

def name_location(soup):
    """Selects all names of town listen in the chosen district."""
    return [location.text for location in soup.find_all("td", {"class": "overflow_name"})]

def code_town(soup):
    """Selects all codes of town listed in the chosen district."""
    return [code.text for code in soup.find_all("td", {"class": "cislo"})]

def parties(url_sub, codes):
    """Fetches party names for town codes."""
    if not codes:
        return []
    url = f"{url_sub}{codes[0]}"
    soup = response_server(url)
    parties_soup = soup.find_all("td", {"class": "overflow_name", "headers" :["t1sa1 t1sb2", "t2sa1 t2sb2"]})
    return [party.text for party in parties_soup]

def fetch_town_data(url):
    """Fetches and cleans data for each town."""
    soup = response_server(url)
    registered = soup.find("td", {"class": "cislo", "headers": "sa2"}).text.replace(" ", "").replace('\xa0', '')
    envelopes = soup.find("td", {"class": "cislo", "headers": "sa3"}).text.replace(" ", "").replace('\xa0', '')
    valid = soup.find("td", {"class": "cislo", "headers": "sa6"}).text.replace(" ", "").replace('\xa0', '')
    votes = soup.find_all("td", {"class": "cislo", "headers": ["t1sa2 t1sb3", "t2sa2 t2sb3"]})
    votes_clean = [vote.text.replace(" ", "").replace('\xa0', '') for vote in votes]
    return registered, envelopes, valid, votes_clean

def data_collector(url_sub, codes, locations, parties):
    """Collects and organizes data for all town."""
    all_data = {"Code": [], "Location": [], "Registered": [], "Envelopes": [], "Valid": []}
    party_data = {party: [] for party in parties}

    for code,location in zip(codes, locations):
        url = f"{url_sub}{code}"
        registered, envelopes, valid, votes_clean= fetch_town_data(url)
         
        all_data["Code"].append(code)
        all_data["Location"].append(location)
        all_data["Registered"].append(registered)
        all_data["Envelopes"].append(envelopes)
        all_data["Valid"].append(valid)

        for i, party in enumerate(parties):
            party_data[party].append(votes_clean[i])

    all_data.update(party_data)
    return all_data

def create_csv(data, csv_file):
    try: 
        df = pd.DataFrame(data)
        print(f"Loading...")
        df.to_csv(csv_file, index= False)
        print(f"Data was saved into file: {csv_file}")
    except Exception as e:
        print(f"Error saving data to CSV: {e}")

def arguments():
    exit_message = "\nExiting program!..."
    if len(sys.argv) != 3:
        print(f"Program needs 2 arguments to run: URL and CSV file name.{exit_message}")
        sys.exit()
    if not sys.argv[1].startswith("https://volby.cz/pls/ps2017nss/"):
        print(f"First argument is not a correct URL.{exit_message}")
        sys.exit()
    if not sys.argv[2].endswith(".csv"):
        print(f"Second argument is not a CSV file name.{exit_message}")
        sys.exit()
    else:
        print(f"Fetching data from: {sys.argv[1]}")

def main():
    arguments()
    csv_file = sys.argv[2]
    url = sys.argv[1]
    base_url = "https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=2&xobec=" 
    soup = response_server(url)
    code = code_town(soup)
    name = name_location(soup)
    party = parties(base_url, code)
    data_final = data_collector(base_url, code, name, party)
    create_csv(data_final, csv_file)

if __name__ == "__main__":
    main()
