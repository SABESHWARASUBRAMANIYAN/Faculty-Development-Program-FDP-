import requests
from bs4 import BeautifulSoup
import csv


URL = "https://annauniv.irins.org/faculty/index/Department+of+Information+Science+and+Technology"
r = requests.get(URL)

soup = BeautifulSoup(r.content,"html5lib") # If this line causes an error, run 'pip install html5lib' or install html5lib
s=soup.find_all("div",class_="cbp-item")

import pandas as pd

#


header = ['Name', 'Designation', 'Subject']
with open("staff_details.csv", mode='a', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=header)


    writer.writeheader()

for i in s:
    m={"Name":i.find("h3").text , "Designation":i.find("span",class_="color-lightYellow").text,"Subject":i.find("span",class_="color-lightWhite").text}
    with open("staff_details.csv", mode='a', newline='') as file:
       
        writer = csv.DictWriter(file, fieldnames=header)
    
        writer.writerow(m)