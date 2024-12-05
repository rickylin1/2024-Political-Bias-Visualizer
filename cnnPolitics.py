# NOTICE: Need to clean the following from scraped content: 
# © 2024 Cable News Network. A Warner Bros. Discovery Company. All Rights Reserved.CNN Sans ™ & © 2016 Cable News Network. For privacy options, please see our privacy policy:https://www.cnn.com/privacy.


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium_stealth import stealth
import requests
from bs4 import BeautifulSoup
import time
import re
from datetime import date
import os

# Get today's date as a string in the format YYYY-MM-DD
today_str = date.today().isoformat()

# Replace hyphens with slashes and add a leading slash
today = "/" + today_str.replace("-", "/")

print(today)

# Initialize headless driver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")


# Initialize the Chrome driver
# driver = webdriver.Chrome(executable_path=driver_path)
try:
    driver = webdriver.Chrome(options=chrome_options)  # Assuming chromedriver is in your PATH

    # Apply stealth settings
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
    )

    url = "https://www.cnn.com/politics"

    # Open the New York Times us news page directory
    driver.get(url)

    # Wait for at least one anchor (stores hyperlinks) tag
    WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))

    # Get the page source after waiting
    webpage_content = driver.page_source

    # Parse the webpage content with BeautifulSoup
    soup = BeautifulSoup(webpage_content, 'html.parser')

    # Find all anchor tags with href containing the date and ending with ".html"
    anchors = soup.find_all('a', href=re.compile(r'.*' + re.escape(today) + r'.*\.html$'))

    # Get href attributes of the found anchor tags
    for anchor in anchors:
        link = f"https://www.cnn.com{anchor['href']}"
        # newlink = f"https://archive.ph/{link}"
        title = anchor["data-zjs-card_name"]
        
        try:
            driver.get(link)
            
            # Wait for page to finish loading
            WebDriverWait(driver, 20).until(lambda d: d.execute_script('return document.readyState') == 'complete')
            
            # Wait for anchor tags
            WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
            
            # Get the page source after waiting
            content = driver.page_source
            
            # Parse the webpage content with BeautifulSoup
            artsoup = BeautifulSoup(content, 'html.parser')
        
            # Find all div elements with the specific style
            article_divs = artsoup.find_all('p')

            # Extract and concatenate the text
            article_text = ''
            for div in article_divs:
                article_text += div.get_text(strip=True) + ' '

            # Clean up the text (remove extra spaces, etc.)
            article_text = ' '.join(article_text.split())

            # Remove the CNN trailing text
            article_text.replace('© 2024 Cable News Network. A Warner Bros. Discovery Company. All Rights Reserved.CNN Sans ™ & © 2016 Cable News Network. For privacy options, please see our privacy policy:https://www.cnn.com/privacy.', '')

            # Generate filename from the original NYT URL
            filename = title + ".txt"
            file_path = os.path.join("cnnPolitics", filename)

            # Check if the file already exists
            if os.path.exists(file_path):
                print(f"Article already exists: {file_path}")
                continue  # Skip to the next article
            
            # Save the article text
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(article_text)
            
            print(f"Article saved to: {file_path}")
        
        except TimeoutException:
            print(f"Timeout occurred while loading {link}")
            continue
        
        time.sleep(5)  # Wait 5 seconds before next request


    print('done')

# Close the browser
finally:
    print('quit')
    driver.quit()
