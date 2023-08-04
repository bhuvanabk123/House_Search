import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep

CHROME_DRIVER_PATH = r'C:\Development\chromedriver.exe'

GOOGLE_FORM = 'https://docs.google.com/forms/d/e/1FAIpQLScMgsWwTTSktXUgOZVeFTbY2iyJhKXGVPhpIDMRvgXdpp1H1w/viewform?usp=sf_link'

ZILLOW_LINK = 'https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22north%22%3A37.908143094647194%2C%22east%22%3A-122.22184268359375%2C%22south%22%3A37.64220165564354%2C%22west%22%3A-122.64481631640625%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A0%2C%22max%22%3A872627%7D%2C%22mp%22%3A%7B%22min%22%3A0%2C%22max%22%3A3000%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22baths%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%2C%22usersSearchTerm%22%3A%22San%20Francisco%20CA%22%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%7D'

headers = {
     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, li   ke Gecko) Chrome/84.0.4147.125 Safari/537.36",
     "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get(ZILLOW_LINK, headers = headers)
zillow_data = response.text

soup = BeautifulSoup(zillow_data, 'html.parser')

addr_link = soup.find_all(name = 'a', class_ = 'property-card-link')
prices = soup.find_all(name = 'span', class_ = 'iMKTKr')



address = []
address_link = []
house_prices = []


for addr in addr_link:
    address.append(addr.getText())
    address_link.append(f"https://www.zillow.com/{addr['href']}")

for price in prices:
    house_prices.append(price.text.split('+')[0])


options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)
service = Service(CHROME_DRIVER_PATH, log_path='NUL')
driver = webdriver.Chrome(options=options, service=service)
driver.get(GOOGLE_FORM)
sleep(10)

for n in range(len(house_prices)):

    addr_response = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(address[n])
    rent_price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(house_prices[n])
    addr_link_response = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(address_link[n])

    submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span').click()

    another_response = driver.find_element(By.LINK_TEXT , 'Submit another response').click()
    sleep(2)


# driver.get('https://docs.google.com/forms/d/e/1FAIpQLScMgsWwTTSktXUgOZVeFTbY2iyJhKXGVPhpIDMRvgXdpp1H1w/viewform?usp=sf_link')
#
# sleep(3)
# sheets = driver.find_element(By.XPATH, '//*[@id="ResponsesView"]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div/span/span[2]').click()
#
#
# destination = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/div[16]/div/div[2]/span/div/div/span/div[1]/label/div/div[2]/div/span').click()
#
# create = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/div[16]/div/div[2]/span/div/div/span/div[1]/label/div/div[2]/div/span').click()
#
#
# sleep(5)



