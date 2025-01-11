import requests
import pytz
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from get_data import create_google_event

json_content_anime = []
# follow_animes = [
#     "dragon ball daima",
#     "Solo Leveling 2nd Season: Arise from the Shadow",
#     "Shangri-La Frontier: Kusoge Hunter, Kamige ni Idoman to su 2nd Season",
#     "Pokémon Horizons: The Series",
#     "Guild no Uketsukejou desu ga, Zangyou wa Iya nanode Boss wo Solo Tobatsu Shiyou to Omoimasu",
#     "One Piece",
#     "Dr. Stone: Science Future",
# ]


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
    hoy = datetime.now()
    week_day = hoy.strftime("%A")
    return week_day


def create_collection(anime_name, anime_local_hour, anime_cap):
    template = {"title": anime_name, "air_time": anime_local_hour, "episode": anime_cap}
    json_content_anime.append(template)


def scrap_web_json():
    url = "https://animeschedule.net/"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        day_now = date_now_day()
        schedule_section = soup.find_all(
            "div", class_=f"timetable-column expanded odd {day_now}"
        )
        if schedule_section:
            for anime in schedule_section:
                anime_card = anime.find_all(
                    "div", class_="timetable-column-show aired expanded"
                )
                for anime_sub_card in anime_card:
                    anime_name = anime_sub_card.find(
                        "h2",
                        class_="show-title-bar",
                    ).text.strip()
                    anime_hour = (
                        anime_sub_card.find("time", class_="show-air-time")
                        .get("datetime")
                        .strip()
                    )
                    anime_cap = anime_sub_card.find(
                        "span", class_="show-episode"
                    ).text.strip()

                    change_time = change_utc_time(anime_hour)
                    current_time = datetime.now()

                    time_change_time = datetime.strptime(
                        change_time, "%Y-%m-%d %I:%M %p"
                    )

                    result = (
                        current_time + timedelta(minutes=10)
                        if time_change_time < current_time
                        else time_change_time
                    )

                    create_collection(
                        anime_name, change_utc_time(anime_hour), anime_cap
                    )
                    # print(result.strftime("%Y-%m-%d %I:%M %p"))
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
print(json_content_anime)
# scrap_web_json()
