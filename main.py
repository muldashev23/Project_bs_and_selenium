from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time


# Your own path where located browser driver. I'm using Chrome. Your webdriver version must be the same as browser ver.
# https://chromedriver.chromium.org/downloads , using this link you can download chromedriver
# Driver must be pre-installed

DRIVER_PATH = "C:\Development\chromedriver.exe"

# Your own http headers
# https://www.whatismybrowser.com/detect/what-http-headers-is-my-browser-sending
# link can help you with info about your browser
HEADER = {
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.82 Safari/537.36 "
}

# Parcing url
URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C" \
      "%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.69219435644531%2C%22east%22%3A-122" \
      ".17446364355469%2C%22south%22%3A37.703343724016136%2C%22north%22%3A37.847169233586946%7D%2C%22isMapVisible%22" \
      "%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D" \
      "%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22" \
      "%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B" \
      "%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price" \
      "%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom" \
      "%22%3A11%7D "

# Chrome driver url
LINK = 'https://docs.google.com/forms/d/e/1FAIpQLSdVAJmvDuyiUT7EWZGw01Mgc3eGAfCYvLbjyjwdJMv2g60TMQ/viewform?usp=sf_link'

# I'm going to parse this link, to find info about homes for rent
# How much they cost, where located and a link to the offer
response = requests.get(url=URL, headers=HEADER)
data = response.text
soup = BeautifulSoup(data, "html.parser")
datas = soup.select(".list-card-info a")
prices = [price.getText() for price in soup.find_all(class_="list-card-price")]
links = []
adresses = []

# Some of parced data have not completed offers link, so just need to add "https://www.zillow.com"
for data in datas:
    link = data.get("href")
    if "https://www.zillow.com" in link:
        links.append(link)

    else:
        link = "https://www.zillow.com" + link
        links.append(link)

    adresses.append(data.getText())

# In this part i'm going to use webdriver to fill the google form with parsed data
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get(LINK)

for n in range(len(prices)):
    time.sleep(3)
    ans_area = driver.find_elements_by_css_selector(".freebirdFormviewerViewItemList input")
    answers = ans_area[0:3]
    adr_in = answers[0]
    pri_in = answers[1]
    lin_in = answers[2]
    btn = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    adr_in.click()
    adr_in.send_keys(adresses[n])
    time.sleep(1)
    pri_in.click()
    pri_in.send_keys(prices[n])
    time.sleep(1)
    lin_in.click()
    lin_in.send_keys(links[n])
    btn.click()
    time.sleep(2)
    btn_ewe = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    btn_ewe.click()
    time.sleep(5)

time.sleep(20)

driver.quit()
