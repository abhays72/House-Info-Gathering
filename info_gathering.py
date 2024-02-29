import requests
from bs4 import BeautifulSoup
from csv import writer
import regex as re

urls = [
    "https://www.zillow.com/homedetails/3477-Glenprosen-Ct-San-Jose-CA-95148/54772104_zpid/",
    "https://www.zillow.com/homedetails/3406-Chemin-De-Riviere-San-Jose-CA-95148/51074974_zpid/",
    "https://www.zillow.com/homedetails/3067-Summerhill-Ct-San-Jose-CA-95148/19792582_zpid/",
    "https://www.zillow.com/homedetails/3515-Rollingside-Dr-San-Jose-CA-95148/19792018_zpid/",
    "https://www.zillow.com/homedetails/3137-Stevens-Ct-San-Jose-CA-95148/19793391_zpid/",
    "https://www.zillow.com/homedetails/3243-Padilla-Way-San-Jose-CA-95148/19792278_zpid/",
    "https://www.zillow.com/homedetails/3515-Rollingside-Dr-San-Jose-CA-95148/19792018_zpid/",
    "https://www.zillow.com/homedetails/2839-Alwood-Ct-San-Jose-CA-95148/19791687_zpid/",
    "https://www.zillow.com/homedetails/3326-Ariel-Joshua-Ct-San-Jose-CA-95135/54772233_zpid/",
    "https://www.zillow.com/homedetails/3042-Pellier-Pl-San-Jose-CA-95135/121043161_zpid/",
]

for url in urls:
    headers = {"User-Agent": "Mozilla/5.0"}
    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.text, "html.parser")

    house_price_data = soup.find_all("span", class_="dpf__sc-1me8eh6-0")
    house_price = ""
    # print(house_price)
    for house in house_price_data:
        house_price = house.text
    house_price = house_price.replace("/mo", "")

    house_info = soup.select('span[data-testid="bed-bath-item"]')
    arr_house_info = (
        []
    )  # duplicates are there so converting arr_house_info into a set and back to remove them
    for textof in house_info:
        arr_house_info.append(textof.text)

    # arr_house_info = list(set(arr_house_info)) #>>>>>>>>

    arr_house_info = arr_house_info[: len(arr_house_info) - 3]

    house_address = url.split("/")
    house_address = house_address[4].replace("-", ", ")
    print(house_address)    
    # house_address = house_address.text.replace("\xa0", "")
    zillow_house_link = url

    umbrella_data = soup.find_all("span", class_="kHeRng")
    # print(umbrella_data)
    data = []
    for lots in umbrella_data:
        data.append(lots.text)

    # regex = re.compile(".*kHeRng.*")
    # for distance in soup.find_all("span", {"class": regex}):
    #     distance_from_school = distance.text
    #     print(distance_from_school.text)

    # distance_from_school = soup.find_all("span", "kHeRng")

    # for distance in distance_from_school:
    #     print(distance.text)
    lot_size = ""

    for data_points in data:
        if "Lot size" in data_points:
            data_points = data_points.replace("Lot size: ", "")
            lot_size = data_points.replace(" sqft", "")

    # phone_number = soup.find("ul", class_="phoneNumber")
    # print(phone_number.text)
    # for numbers in phone_number:
    #     print("HI")
    #     print(numbers.text)

    info_dict = {}

    keys = soup.find_all("span", class_="dpf__sc-2arhs5-2")
    values = soup.find_all("span", class_="dpf__sc-2arhs5-3")

    for i in range(len(keys)):
        info_dict[keys[i].text] = values[i].text

    # EXPORTING info_dict TO FILE
    info_dict_values = []
    for value in info_dict.values():
        info_dict_values.append(value)

    info_dict_values.extend([house_address, zillow_house_link, lot_size])
    last_info_dict_values = info_dict_values + arr_house_info

    # print(last_info_dict_values)

    with open("houses.csv", "a") as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(last_info_dict_values)
        f_object.close()
