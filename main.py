from pprint import pprint

import requests
import datetime
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

CLIENTID = os.environ.get('SPOTIPY_CLIENT_ID')
SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')
URI = os.environ.get('SPOTIPY_REDIRECT_URI')

date_now = datetime.date.today()
oldest_date = datetime.date(1958, 8, 4)
year_now = date_now.year

print(os)


def get_date():
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    check = True
    year = 0
    month = 0
    day = 0
    while check:
        print("Which year would you like music from? ")
        try:
            year = int(input())
            if year > year_now:
                raise ValueError()
            check = False
        except ValueError:
            print(f"Please enter a valid year between 1958 and {year_now}.")
    if year % 4 == 0:
        month_days[1] == 29
    check = True
    while check:
        print("Which month would you like music from (1-12)? ")
        try:
            month = int(input())
            if not 1 <= month <= 12:
                print("A")
                raise ValueError()
            check = False
        except ValueError:
            print(f"Please enter a valid month as a number from 1 to 12.")
    check = True
    while check:
        print("Which day would you like music from? ")
        try:
            day = int(input())
            if day < 1 or day > month_days[month - 1]:
                print("A")
                raise ValueError()
            check = False
        except ValueError:
            print(f"Please enter a valid month as a number from 1 to {month_days[month - 1]}.")
    return datetime.date(year, month, day)


chosen_date = get_date()
while not date_now >= chosen_date >= oldest_date:
    print("The date you selected was not valid. Please choose a date between 4 August 1958 and today.")
    print(chosen_date)
    chosen_date = get_date()
site = requests.get(
    url=f"https://www.billboard.com/charts/hot-100/{chosen_date.year:04d}-{chosen_date.month:02d}-{chosen_date.day:02d}")
soup = BeautifulSoup(site.text, "html.parser")
raw_titles = soup.find_all(id="title-of-a-story", name="h3", class_="c-title a-no-trucate a-font-primary-bold-s "
                                                                    "u-letter-spacing-0021 lrv-u-font-size-18@tablet "
                                                                    "lrv-u-font-size-16 u-line-height-125 "
                                                                    "u-line-height-normal@mobile-max "
                                                                    "a-truncate-ellipsis u-max-width-330 "
                                                                    "u-max-width-230@tablet-only")
titles = [soup.find(id="title-of-a-story", name="h3", class_="c-title a-no-trucate a-font-primary-bold-s "
                                                             "u-letter-spacing-0021 u-font-size-23@tablet "
                                                             "lrv-u-font-size-16 u-line-height-125 "
                                                             "u-line-height-normal@mobile-max a-truncate-ellipsis "
                                                             "u-max-width-245 u-max-width-230@tablet-only "
                                                             "u-letter-spacing-0028@tablet").get_text()[1:-1]]
for i in raw_titles:
    titles.append(i.get_text()[1:-1])

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENTID, client_secret=SECRET, redirect_uri=URI))

results = sp.search(type='track', q=titles[1])
pprint(results["tracks"]["items"][0]["name"])
print(titles[1])
tracks=[]
#sp.user_playlist_add_tracks(user='jxaweaogwz7q2todcaaaphcky', playlist_id='', tracks=tracks, position=None)
#sp.user_playlist_create(user='jxaweaogwz7q2todcaaaphcky', name=f'Hits from {chosen_date.year:04d}-{chosen_date.month:02d}-{chosen_date.day:02d}', public=True, description=f'The top 100 songs on the billboard on {chosen_date.year:04d}-{chosen_date.month:02d}-{chosen_date.day:02d}')