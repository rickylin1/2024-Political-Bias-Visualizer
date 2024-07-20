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

    url = "https://www.nytimes.com/section/world"

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
    # plug into https://archive.ph/
    # id="CONTENT"
    # style="display:block;color:blue
    for anchor in anchors:
        link = f"https://www.nytimes.com{anchor['href']}"
        newlink = f"https://archive.ph/{link}"
        title = anchor.get_text()
        
        try:
            driver.get(newlink)
            
            # Wait for page to finish loading
            WebDriverWait(driver, 20).until(lambda d: d.execute_script('return document.readyState') == 'complete')
            
            # Wait for anchor tags
            WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
            
            # Get the page source after waiting
            content = driver.page_source
            
            # Parse the webpage content with BeautifulSoup
            newsoup = BeautifulSoup(content, 'html.parser')
            
            # Find all anchor tags with style containing "display:block;color:blue"
            newanchors = newsoup.find_all('a', style=lambda value: value and 'display:block' in value and 'color:blue' in value)
            
            if(len(newanchors) == 1):
                print(newanchors[0]['href'])
            
                driver.get(newanchors[0]['href'])
                
                # Wait for page to finish loading
                WebDriverWait(driver, 20).until(lambda d: d.execute_script('return document.readyState') == 'complete')

                # Get the page source after the page has loaded
                page_source = driver.page_source

                # Parse with BeautifulSoup
                artsoup = BeautifulSoup(page_source, 'html.parser')

                # Find all div elements with the specific style
                article_divs = artsoup.find_all('div', style=lambda value: value and 
                                            'color:rgb(54, 54, 54)' in value and 
                                            'font-family:nyt-imperial' in value)

                # Extract and concatenate the text
                article_text = ''
                for div in article_divs:
                    article_text += div.get_text(strip=True) + ' '

                # Clean up the text (remove extra spaces, etc.)
                article_text = ' '.join(article_text.split())

                # Generate filename from the original NYT URL
                filename = title + ".txt"
                file_path = os.path.join("nytimesWorldNews", filename)

                # Check if the file already exists
                if os.path.exists(file_path):
                    print(f"Article already exists: {file_path}")
                    continue  # Skip to the next article
                
                # Save the article text
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(article_text)
                
                print(f"Article saved to: {file_path}")
        
        except TimeoutException:
            print(f"Timeout occurred while loading {newlink}")
            continue
        
        time.sleep(5)  # Wait 5 seconds before next request


    print('done')

# Close the browser
finally:
    print('quit')
    driver.quit()
