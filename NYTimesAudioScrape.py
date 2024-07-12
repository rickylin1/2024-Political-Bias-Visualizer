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
    audio_links = []
    for anchor in anchors:
        page_link = "https://www.nytimes.com" + anchor['href']
        driver.get(page_link)
        
        try:
            
            button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@title="Play Audio" and @aria-label="Play Audio"]')))
            # Click the button
            button.click()

            # Wait for the audio element to appear after clicking the button
            WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'audio')))
        
        except Exception as e:
            print(f"An error occurred: {e}")
        
        # Get the page source after waiting
        page_content = driver.page_source

        # Parse the new page content with BeautifulSoup
        page_soup = BeautifulSoup(page_content, 'html.parser')

        # Find the audio tag and extract its src attribute
        audio_tags = page_soup.find_all('audio')
        
        for audio_tag in audio_tags:
            if 'src' in audio_tag.attrs:
                audio_src = audio_tag['src']
                audio_links.append(audio_src)

        print(f"Visiting: {page_link}")
    
    print(audio_links)

    print('done')

# Close the browser
finally:
    print('quit')
    driver.quit()
