import requests
import pytz
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from get_data import create_google_event
from function_time import change_time_peru, transform_format_twelve_str

json_content_anime = []


def read_file_animes():
    with open("./list_animes.txt", "r", encoding="utf-8") as file:
        anime_list = [line.strip() for line in file]
    return anime_list


follow_animes = read_file_animes()


def change_utc_time(utc_time_str):
    utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%MZ")

    utc_zone = pytz.utc
    utc_time = utc_zone.localize(utc_time)

    peru_zone = pytz.timezone("America/Lima")
    local_time = utc_time.astimezone(peru_zone)
    return local_time.strftime("%Y-%m-%d %I:%M %p")


def date_now_day():
    days_week_even = ["Tuesday", "Thursday", "Saturday"]
    hoy = datetime.now()
    week_day = hoy.strftime("%A")
    if week_day in days_week_even:
        return f"even {week_day}"
    else:
        return f"odd {week_day}"


def create_collection(anime_name, anime_local_hour, anime_cap):
    template = {"title": anime_name, "air_time": anime_local_hour, "episode": anime_cap}
    json_content_anime.append(template)


def aired_unaired(anime, opt_cap):
    anime_card = anime.find_all(
        "div", class_=f"timetable-column-show {opt_cap} expanded"
    )
    for anime_sub_card in anime_card:
        anime_name = anime_sub_card.find("h2", class_="show-title-bar").text.strip()
        anime_hour = (
            anime_sub_card.find("time", class_="show-air-time").get("datetime").strip()
        )
        anime_cap = anime_sub_card.find("span", class_="show-episode").text.strip()
        change_time = change_time_peru(anime_hour)
        current_time = datetime.now(pytz.timezone("America/Lima"))
        result = (
            current_time + timedelta(minutes=10)
            if change_time < current_time
            else change_time
        )
        create_collection(anime_name, transform_format_twelve_str(result), anime_cap)


def save_as_json():
    file_path = "./animes_hoy.json"
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(json_content_anime, file, indent=4, ensure_ascii=False)


def scrap_web_json():
    url = "https://animeschedule.net/"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        day_now = date_now_day()
        schedule_section = soup.find_all(
            "div", class_=f"timetable-column expanded {day_now}"
        )
        if schedule_section:
            for anime in schedule_section:
                aired_unaired(anime, "aired")
                aired_unaired(anime, "unaired")
        save_as_json()
    else:
        print(f"Error al acceder a la pagina: {response.status_code}")


def temp_follow_anime():
    scrap_web_json()
    for anime in json_content_anime:
        for follow_anime in follow_animes:
            if follow_anime.lower() in anime["title"].lower():
                create_google_event(anime)
                # print(anime)


temp_follow_anime()
# print(json_content_anime)
# scrap_web_json()
