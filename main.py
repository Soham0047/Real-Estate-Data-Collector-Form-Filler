from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Setting up the request headers
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

# Sending a GET request to the Zillow-Clone page
response = requests.get("https://appbrewery.github.io/Zillow-Clone/", headers=headers)
web_content = response.text

# Parsing the HTML content
soup = BeautifulSoup(web_content, "html.parser")

# Extracting property links
property_links = [link["href"] for link in soup.select(".StyledPropertyCardDataWrapper a")]
print(f"Total property links found: {len(property_links)}")
print(property_links)

# Extracting property addresses
property_addresses = [addr.get_text().replace(" | ", " ").strip() for addr in
                      soup.select(".StyledPropertyCardDataWrapper address")]
print(f"\nCleaned addresses ({len(property_addresses)}):")
print(property_addresses)

# Extracting property prices
property_prices = [price.get_text().replace("/mo", "").split("+")[0] for price in
                   soup.select(".PropertyCardWrapper span") if "$" in price.text]
print(f"\nCleaned prices ({len(property_prices)}):")
print(property_prices)

# Part 2 - Automating form filling with Selenium

# Setting up Chrome browser options
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
browser = webdriver.Chrome(options=options)

# Looping through the properties and filling out the form
for i in range(len(property_links)):
    browser.get("YOUR_GOOGLE_FORMS_LINK")
    time.sleep(2)

    # Locating form input fields using XPath
    address_input = browser.find_element(By.XPATH,
                                         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input = browser.find_element(By.XPATH,
                                       '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input = browser.find_element(By.XPATH,
                                      '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = browser.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

    # Filling in the form fields
    address_input.send_keys(property_addresses[i])
    price_input.send_keys(property_prices[i])
    link_input.send_keys(property_links[i])

    # Submitting the form
    submit_button.click()
