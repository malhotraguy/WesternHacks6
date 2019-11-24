import requests

from helper import get_credentials

creds = get_credentials("./secrets/giphy_credentials.json")
api_key = creds["api_key"]


def get_giphy(person_name, tweet, gif_type):
    url = f"https://api.giphy.com/v1/gifs/translate?api_key={api_key}&s={person_name}:{tweet}"
    resp = requests.get(url=url)
    data = resp.json()
    giphy_url = data.get("data").get("images").get(gif_type).get("url")
    return giphy_url
