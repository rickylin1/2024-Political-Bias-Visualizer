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


try:
    driver = webdriver.Chrome()  
    url = "https://www.cnn.com/audio/podcasts/inside-politics"
    driver.get(url)
    load_more_button = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.ID, "load-more"))
    )

    for i in range(3):
        driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
        load_more_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.ID, "load-more"))
        )
        load_more_button.click()

    print("Clicked on the 'Show more episodes' button")

     # Get the page source after waiting
    webpage_content = driver.page_source

    # Parse the webpage content with BeautifulSoup
    soup = BeautifulSoup(webpage_content, 'html.parser')
    elements = soup.find_all(class_='episode')

    audio_urls = []

    for element in elements:
        src = element.get('src')
        if src:
            audio_urls.append(src)

    print(audio_urls)


    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(script_dir, 'urls.txt')

    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            for url in audio_urls:
                f.write(url + '\n')
    else:
        print(f"The file '{file_path}' already exists. Skipping creation.")

    print(f"URLs written to '{file_path}'.")
    print('done')

finally:
    print('quit')
    driver.quit()
