from bs4 import BeautifulSoup as bs
import requests
import argparse

# Text parser
parser = argparse.ArgumentParser(description="Quick Script for Extracting Weather data using Google Weather")
parser.add_argument("region", nargs="?", help="""Region to get weather for, must be available region.
                                    Default is your current location determined by your IP Address""", default="")

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
LANGUAGE = "en-US, en; q=0.5"


def get_weather_data(url):

    session = requests.Session()

    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE

    html = session.get(url)
    soup = bs(html.text, "html.parser")

    # store all results on this dictionary
    result = {}

    result['region'] = soup.find("div", attrs={"id": "wob_loc"}).text
    result['temp_now'] = soup.find("span", attrs={"id": "wob_tm"}).text
    result['dayhour'] = soup.find("div", attrs={"id": "wob_dts"}).text
    result['weather_now'] = soup.find("span", attrs={"id": "wob_dc"}).text
    result['precipitation'] = soup.find("span", attrs={"id": "wob_pp"}).text
    result['humidity'] = soup.find("span", attrs={"id": "wob_hm"}).text
    result['wind'] = soup.find("span", attrs={"id": "wob_ws"}).text

    next_days = []
    days = soup.find("div", attrs={"id": "wob_dp"})

    for day in days.findAll("div", attrs={"class": "wob_df"}):
        day_name = day.findAll("div")[0].attrs['aria-label']
        weather = day.find("img").attrs["alt"]
        temp = day.findAll("span", {"class": "wob_t"})
        max_temp = temp[0].text
        min_temp = temp[2].text
        next_days.append({"name": day_name, "weather": weather, "max_temp": max_temp, "min_temp": min_temp})

    result['next_days'] = next_days

    return result


def get_result(search):

    URL = f"https://www.google.com/search?q={search}+weather"

    args = parser.parse_args()
    region = args.region
    URL += region
    data = get_weather_data(URL)

    # print data
    print("\n")
    print("-"*40)
    print("\n")

    print("Weather for:", data["region"])
    print("\n")
    print("Time:", data["dayhour"])
    print(f"Temperature now: {data['temp_now']}°C")
    print("Description:", data['weather_now'])
    print("Precipitation:", data["precipitation"])
    print("Humidity:", data["humidity"])
    print("Wind:", data["wind"])

    print("\n")
    for dayweather in data["next_days"]:
        print("-"*10, dayweather["name"], "-"*10)
        print("Description:", dayweather["weather"])
        print(f"Max temperature: {dayweather['max_temp']}°C")
        print(f"Min temperature: {dayweather['min_temp']}°C")
        print("\n")