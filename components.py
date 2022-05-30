from bs4 import BeautifulSoup
import requests
import time
import csv
from selenium import webdriver

# Header for BeautifulSoup
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}
# Link to form and chrome driver
address_entry = "https://docs.google.com/forms/d/e/1FAIpQLScwXU88Xj1884lB0ygRK7MYaJ3JmhQLmm5lyzGit6rei0zV5g/viewform?usp=sf_link"
chrome_driver_path = "C:\Development\chromedriver.exe"

class Components:
    def __init__(self, city, state):
        # Store addresses, prices, and links
        self.cities = []
        self.states = []
        self.addresses = []
        self.prices = []
        self.links = []

        # Store locations
        self.city = ""
        self.state = ""
        self.get_location(city, state)

        try:
            # Store link of city of property
            self.properties = f"https://www.zillow.com/homes/{city},-{state}_rb/"
            self.get_properties()
        except:
            print("Invalid driver path or Chrome Driver version!")

        try:
            # Enter data
            self.driver = webdriver.Chrome(executable_path=chrome_driver_path)
            self.enter_data()
            self.save_data()
        except:
            print("Invalid ")

    def get_location(self, city, state):
        new_city = ""
        part_of_city = ""

        for i in range(0, len(city)):
            if city[i] == ' ':
                part_of_city = part_of_city.title()
                new_city += part_of_city
                new_city += ' '
                part_of_city = ''

            else:
                part_of_city += city[i]
        new_city += part_of_city.title()

        # Name of city and capital state abbreviation
        self.city = new_city.title()
        self.state = str.upper(state)

    def get_properties(self):
        # Request BeautifulSoup
        resp = requests.get(self.properties, headers=header)
        page = resp.text
        soup = BeautifulSoup(page, 'html.parser')

        # Get addresses and prices
        addresses = soup.select(".list-card-info address")
        self.addresses = [address.text for address in addresses]
        prices = soup.select(".list-card-heading div")
        self.prices = [price.text.split("/")[0].split("+")[0] for price in prices]

        # Get links and store as a new link if 'http' not present, else copy link in 'href'
        links = soup.select(".list-card-info a")
        for link in links:
            if "http" not in link['href']:
                self.links.append(f"https://www.zillow.com{link['href']}")
            else:
                self.links.append(link["href"])

            # Add cities and states too
            self.cities.append(self.city)
            self.states.append(self.state)

    def enter_data(self):
        if len(self.addresses) > 0:
            # For each address, enter data
            for i in range(0, len(self.addresses)):
                # Open page every time
                self.driver.get(address_entry)
                time.sleep(3)

                # Enter city
                enter_city = self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
                enter_city.send_keys(self.cities[i])
                time.sleep(3)

                # Enter state abbreviation
                enter_state = self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
                enter_state.send_keys(self.states[i])
                time.sleep(3)

                # Enter address
                enter_address = self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
                enter_address.send_keys(self.addresses[i])
                time.sleep(3)

                # Enter price
                enter_price = self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input')
                enter_price.send_keys(self.prices[i])
                time.sleep(3)

                # Enter link
                enter_link = self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div/div[1]/input')
                enter_link.send_keys(self.links[i])
                time.sleep(3)

                # Submit data
                button = self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
                button.click()
                time.sleep(3)
        else:
            print(f"No properties found in {self.city}, {self.state}")

    def save_data(self):
        with open("house_prices.csv", "w", newline='', encoding="utf-8") as file:
            # Write title of columns
            column_titles = ['City', 'State', 'Address', 'Price', 'Link']
            writer = csv.writer(file)
            writer.writerow(column_titles)

            # Write each row
            for i in range(0, len(self.cities)):
                row = [self.cities[i], self.states[i], self.addresses[i], self.prices[i], self.links[i]]
                writer.writerow(row)