from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import time
import re

##javascript in dom to see all podcasts for NYTImes
# // Select all anchor elements in the document
# const anchors = document.getElementsByTagName('a');

# // Iterate over each anchor element
# Array.from(anchors).forEach(anchor => {
#     // Get the value of href attribute
#     const href = anchor.getAttribute('href');

#     // Check if href contains "podcasts" and ends with ".html"
#     if (href && href.includes('podcasts') && href.endsWith('.html')) {
#         // Print or do whatever you want with the anchor element
#         console.log(anchor);
#     }
# });


# Initialize the Chrome driver
# driver = webdriver.Chrome(executable_path=driver_path)
try:
    driver = webdriver.Chrome()  # Assuming chromedriver is in your PATH
    url = "https://www.nytimes.com/column/the-headlines"

    # Open the New York Times audio page directory
    driver.get(url)

    WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))

     # Get the page source after waiting
    webpage_content = driver.page_source

    # Parse the webpage content with BeautifulSoup
    soup = BeautifulSoup(webpage_content, 'html.parser')

    # Find all anchor tags with href containing "podcasts" and ending with ".html"
    anchors = soup.find_all('a', href=re.compile(r'podcasts.*\.html$'))

    # Print the href attributes of the found anchor tags
    for anchor in anchors:
        print(anchor['href'])


    # Optionally, maximize the window
    driver.maximize_window()

    # Keep the browser open for a while to see the page
    time.sleep(10)  # Sleep for 10 seconds

    response = requests.get(url)

    # if response.status_code == 200:
    #     webpage_content = response.text

    #     # Parse the webpage content with BeautifulSoup
    #     soup = BeautifulSoup(webpage_content, 'html.parser')

    #     # Find all anchor tags with href containing "podcasts" and ending with ".html"
    #     anchors = soup.find_all('a', href=re.compile(r'podcasts.*\.html$'))

    #     # Print the href attributes of the found anchor tags
    #     for anchor in anchors:
    #         print(anchor['href'])
    # else:
    #     print(f"Failed to retrieve the webpage. Status code: {response.status_code}")


    print('done')

# Close the browser
finally:
    print('quit')
    driver.quit()
