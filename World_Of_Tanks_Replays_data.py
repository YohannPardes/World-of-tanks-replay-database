from bs4 import BeautifulSoup
from os import system
from selenium import webdriver
import requests
import csv
import os.path

def is_internet_connected(trys = 1):
     """check if internet is connected
     
     return True or False"""

     system("cls")
     if trys < 0:
          # raise ValueError ("Not internet connecton found")
          return False

     url = "http://www.google.com"
     timeout = 1
     try:
          request = requests.get(url, timeout=timeout)
          print("Connected to the Internet")
          return True

     except (requests.ConnectionError, requests.Timeout) as exception:
          print(f"No internet connection. {trys + 1}")
          sleep(5)
          is_internet_connected(trys - 1)

def updated_chromium(options):

    # selenium 4
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.utils import ChromeType

    driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options = options)

    return driver


# setting up the options for the chrome driver
options = webdriver.ChromeOptions()
options.add_argument('headless')

# checking if there is an internet connection
if is_internet_connected():
     # create the driver
     driver = updated_chromium(options)


def get_urls(driver, nb_pages):

     """get the url's of all the replays"""
     list_of_url = []
     #scrapp the html source page
     for i in range(nb_pages): #there are thousands of pages
          print(f"url listing - {i/nb_pages:2%}")
          main_URL = f"http://wotreplays.eu/site/index/version/104/battle_type/1/sort/uploaded_at.desc/page/{i+111}/"
          driver.get(main_URL)
          content = driver.page_source 

          #managing the html to get the relevant data
          soup = BeautifulSoup(content, features = "html.parser")
     
          matches = soup.findAll("a", class_="link--pale_orange")

          #getting the urls of the replays
          for match in matches:
               list_of_url.append("http://wotreplays.eu" + match.get("href"))

     return list_of_url

def get_data_replays(list_of_urls):

     """extracting the data of each replay separateley"""

     games_data = []
     for i, url in enumerate(list_of_urls):
          print(f"extracting data - {i/len(list_of_urls):5%}")
          single_game_data = []
          driver.implicitly_wait(0.2)
          driver.get(url)
          
          content = driver.page_source
          soup = BeautifulSoup(content, features = "html.parser")

          def find_team_data():

               players_data = soup.findAll("td", class_="team-table__tank")

               team_1 = []
               for data in players_data[:15]:
                    team_1.append(data.get("title"))

               team_2 = []
               for data in players_data[15:]:
                    team_2.append(data.get("title"))

               return team_1, team_2

          def find_game_state_data():
               
               game_title = soup.findAll("div", class_="replay-stats__title")

               state = str(game_title)
               state = state.replace("""[<div class="replay-stats__title">""", "")
               state = state.replace("""</div>]""", "")

               return state

          state = find_game_state_data()
          if state != "[]":
               
               team_1, team_2 = find_team_data()

               single_game_data.append(state)
               single_game_data.append(team_1)
               single_game_data.append(team_2)

          
               save_data_to("csv", single_game_data)

     # print(*games_data, sep = "\n\n\n")

def save_data_to(to_type, data):

     if to_type == "csv":
          if not os.path.exists("data.csv"):
               with open("data.csv", "w") as file:
                    writer = csv.writer(file)
                    writer.writerow(["RESULT", "T11", "T12", "T13", "T14", "T15", "T16", "T17", "T18", "T19", "T110", "T111",
                         "T112", "T113", "T14", "T15", "T21", "T22", "T23", "T24", "T25", "T26", "T27", "T28", "T29", "T210", "T211", "T212", "T213,"
                         "T214", "T215"])

          with open("data.csv", "a", encoding="utf-8") as file:

               writer = csv.writer(file)
               csv_data = [data[0]] + data[1] + data[2]
               writer.writerow(csv_data)


url_list = get_urls(driver, 390)

get_data_replays(url_list)

driver.close()
