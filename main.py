import json
import requests
import sqlite3

URL = "https://net-secondary.web.minecraft-services.net/api/v1.0/en-us/search?sortType=Recent&category=Marketplace&filter%5BpackType%5D="
headers = {"User-Agent": "Mozilla/5.0"}  # Default header is just python so server will think we are a bot. Put user-agent header used to larp as real user.

def main():
    filters = finding_filters()
    sqliteStorage(filters)
    return None

def scraping(URL, headers):
# Takes in our target URL and headers, spits out our scraped json file

    getInfo = requests.get(URL, headers = headers) # Sends https request for our info to target URL
    getInfo.raise_for_status()
    data = getInfo.json()
    return data


def finding_filters():
# Finding our filters (pack types) to scrape for
    # Found this URL under network tab when using inspect element on Minecraft Marketplace Website
    # Contains the diff pack types we can filter thru, store this as array and loop over it when making api request to get diff pack info

    filters = "https://net-secondary.web.minecraft-services.net/api/v1.0/en-us/filters"
    packTypes = (scraping(filters, headers)["result"]["marketplace"][0]["values"])
    return packTypes


def sqliteStorage(filters):
# Function to store our different packs in sql database

    try:
        with sqlite3.connect("MarketPlace.db") as conn:
            print("Opened DB!")
            cursor = conn.cursor()

# This first table contains our static info (attributes of packs that do not change)
# Since we are scraping every week, it will be storage efficent to keep this seperate from other attributes that change
            create_static_table = """
                CREATE TABLE IF NOT EXISTS packs 
                (
                    pack_id     TEXT PRIMARY KEY, -- our primary key for database since its unique to every pack
                    title       TEXT NOT NULL,
                    author      TEXT,
                    pack_type   TEXT,
                    url         TEXT,
                    first_seen  TEXT
                );
            """

# This is the second table containing our time-series dynamic info
            create_dynamic_table = """
            CREATE TABLE IF NOT EXISTS snapshots
            (
                    pack_id     TEXT NOT NULL,
                    scrape_date TEXT NOT NULL,
                    price       REAL,
                    rating      REAL,
                    num_reviews NONE,
                    PRIMARY KEY (pack_id, scrape_date),
                    FOREIGN KEY (pack_id) REFERENCES packs(pack_id)
            );
            """

            cursor.execute(create_static_table)
            cursor.execute(create_dynamic_table)
            conn.commit()

    except sqlite3.OperationalError as e:
        print("Couldn't open ", e)
    return None

if __name__ == "__main__":
    main()