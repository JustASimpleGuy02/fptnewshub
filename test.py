from selenium import webdriver
import time

# start web browser
browser=webdriver.Chrome()

# get source code
browser.get("https://www.google.com/search?q=đại+học+fpt+site:cand.com.vn&num=100&start=0")
time.sleep(100)
html = browser.page_source
print(html)

# close web browser
browser.close()