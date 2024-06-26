from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.support.wait import WebDriverWait

# URL of the website you want to scrape
url = 'https://www.google.com/maps/dir///'

# Source and destination city names
source_city = "Mysuru"
destination_city = "Mangaluru"

# Initialize a Chrome webdriver (you need to have ChromeDriver installed)
driver = webdriver.Chrome()

# Open the website in the browser
driver.get(url)

time.sleep(3)

# Find all input fields with the specified class name
input_fields = driver.find_elements(By.CLASS_NAME, 'tactile-searchbox-input')

# Assuming the source city input is the first one and destination city input is the second one
# Clear any existing text in both input fields
time.sleep(2)
input_fields[0].clear()
input_fields[1].clear()

# Enter source city name into the first input field
input_fields[0].send_keys(source_city)

# Enter destination city name into the second input field
input_fields[1].send_keys(destination_city)

# Wait for a few seconds for the autocomplete suggestions to appear (if any)
time.sleep(4)

# Press Enter key to submit the input in the destination city input field
input_fields[1].send_keys(Keys.ENTER)

# Wait for a few seconds for the page to load after submitting the input
time.sleep(4)

# button = driver.find_element(By.CLASS_NAME, 'm6Uuef')

# Click the button
# button.click()

driving_time_element = driver.find_element(By.CLASS_NAME, 'Fk3sm')
print("Driving Time: " + str(driving_time_element.text))

distance = driver.find_element(By.CLASS_NAME, "ivN21e")
print("Distance: " + str(distance.text))

route_via = driver.find_element(By.CLASS_NAME, "VuCHmb")
print("Route Via: " + str(route_via.text))

traffic_status = driver.find_element(By.CLASS_NAME, "JxBYrc")
print("Traffic Status: " + str(traffic_status.text))
# Get the HTML content of the page
#html_content = driver.page_source

# Close the browser
driver.quit()

# Print the HTML content
#print(html_content)
