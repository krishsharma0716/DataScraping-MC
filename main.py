import json
import requests
import sqlite3

def main():
    # Finding our filters to scrape for
        # Found this URL under network tab when using inspect element on Minecraft Marketplace Website
        # Contains the diff pack types we can filter thru, store this as array and loop over it when making api request to get diff pack info

    filters = "https://net-secondary.web.minecraft-services.net/api/v1.0/en-us/filters"
    # Header for sending .get request to server (basically telling server we aren't a bot so we dont get blocked)
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Safari/605.1.15"}
    packTypes = (scraping(filters, headers)["packType"])

    #Database for each packtype
    for packType in packTypes:
        URL = "https://net-secondary.web.minecraft-services.net/api/v1.0/en-us/search?sortType=Recent&category=Marketplace&filter%5BpackType%5D=" + packType
        data = scraping(URL, headers)

def scraping(URL, headers):
    #takes in our target URL and headers
    #spits out our scraped json file

    getInfo = requests.get(URL, headers = headers)
    data = getInfo.json()
    return data

if __name__ == "__main__":
    main()