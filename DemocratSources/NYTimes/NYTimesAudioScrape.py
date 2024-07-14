from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import os


try:
    driver = webdriver.Chrome()  
    url = "https://www.nytimes.com/column/the-headlines"
    driver.get(url)

    WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))

    webpage_content = driver.page_source

    soup = BeautifulSoup(webpage_content, 'html.parser')

    # Find all anchor tags with href containing "podcasts" and ending with ".html"
    anchors = soup.find_all('a', href=re.compile(r'podcasts.*\.html$'))

    audio_links = []
    for anchor in anchors:
        page_link = "https://www.nytimes.com" + anchor['href']
        driver.get(page_link)
        
        try:
            button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@title="Play Audio" and @aria-label="Play Audio"]')))
            button.click()
            WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'audio')))
        
        except Exception as e:
            print(f"An error occurred: {e}")
        
        page_content = driver.page_source
        page_soup = BeautifulSoup(page_content, 'html.parser')
        audio_tags = page_soup.find_all('audio')
        
        for audio_tag in audio_tags:
            if 'src' in audio_tag.attrs:
                audio_src = audio_tag['src']
                audio_links.append(audio_src)

        # print(f"Visiting: {page_link}")
    
    print(audio_links)
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(script_dir, 'urls.txt')

    # Check if the file already exists
    if not os.path.exists(file_path):
        # If it doesn't exist, create it and write the URLs
        with open(file_path, 'w') as f:
            for url in audio_links:
                f.write(url + '\n')
    else:
        print(f"The file '{file_path}' already exists. Skipping creation.")

    print(f"URLs written to '{file_path}'.")

    print('done')

finally:
    print('quit')
    driver.quit()
