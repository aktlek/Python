from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
import time

def scroll(driver, timeout):
    scroll_pause_time = timeout

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same it will exit the function
            break
        last_height = new_height


#Options for browser
options = Options()
options.headless = True


#Starting hidden browser
browser=webdriver.Firefox(options=options)
browser.implicitly_wait(30)
browser.get("https://www.ozon.ru/category/sportivnoe-pitanie-11650/")

scroll(browser, 5)

time.sleep(5)


#extracting data from browser
soup = BeautifulSoup(browser.page_source, 'html.parser')


#closing browser
browser.close()

#getting parsing data from web page
prices = soup.find_all('div',class_='a0s9')

# open file to export
f = open("result.csv", "w")


#exporting files
for price in prices:
    child = price.find('a',class_='a2g0', href=True)
    f.write(child.get_text())
    f.write('\t')
    f.write("https://www.ozon.ru" + child['href'][:child['href'].find('/?asb=')+1])
    span = price.find('span',class_=['b5v6 b5v7 c4v8','b5v6 b5v7'])
    f.write('\t')
    f.write(str(span.text))
    f.write('\n')
f.close()
