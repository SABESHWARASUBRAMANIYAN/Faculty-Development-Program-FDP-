from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager  # Import for Chrome
import re
# Create a WebDriver instance using WebDriver Manager (Chrome in this example)
def client(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())

    # Navigate to the webpage where you want to extract elements
    # Replace with the URL of your target page
    driver.get(url)

    # Function to scroll down to load more content
    def scroll_down():
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.implicitly_wait(2)  # Use implicit wait to allow content to load

    # Scroll down multiple times to load more content
    for _ in range(10):  # Adjust the number of times you want to scroll
        scroll_down()
    import time
    time.sleep(10)
    # Find elements with the specified class name
    elements = driver.find_elements(By.CLASS_NAME, "panel.panel-profile.margin-bottom-10")

    # Extract and print the text content of the found elements
    # Get the HTML content of the element
    element_html = elements[0].get_attribute("outerHTML")
    from bs4 import BeautifulSoup

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(element_html, 'html.parser')

    # Now you can work with the parsed HTML using Beautiful Soup functions
    s=soup.find_all(class_="row")
    f=[]
    for i in s:
    
        ans=[]
        l=re.findall(rf"Year (\d+)",i.get_text())
        ans.append(l[0])
        ans.append(i.find("span",class_="label label-info").text)
        ans.append(i.find("h2").text)
        f.append(ans)

    # Close the WebDriver

    driver.quit()
    return f
