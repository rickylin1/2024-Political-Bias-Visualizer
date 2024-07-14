from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import os
import time
import YTScrape


try:
    driver = webdriver.Chrome()  
    url = "https://www.youtube.com/@FoxNews/videos"
    driver.get(url)
    #scroll to get videos from past week give or take
    scroll_count = 10
    while scroll_count > 0:
        driver.execute_script('window.scrollBy(0, window.innerHeight);')
        scroll_count -= 1

    time.sleep(10)



     # Get the page source after waiting
    webpage_content = driver.page_source

    soup = BeautifulSoup(webpage_content, 'html.parser')

    elements = soup.find_all(id='video-title-link') 

    audio_urls = []

    for element in elements:
        href = element.get('href')
        if href:
            youtube_url = "https://www.youtube.com" + href
            mp3_url = YTScrape.get_mp3_url(youtube_url)
            audio_urls.append(mp3_url)

    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(script_dir, 'urls.txt')

    existing_urls = set()

    # Check existing urls in the file
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            for line in f:
                existing_urls.add(line.strip())

    # Write new urls to the file
    with open(file_path, 'a') as f:
        for url in audio_urls:
            if url not in existing_urls:
                f.write(url + '\n')
                existing_urls.add(url)

    print(f"URLs written to '{file_path}'.")
    print('done')

finally:
    print('quit')
    driver.quit()
