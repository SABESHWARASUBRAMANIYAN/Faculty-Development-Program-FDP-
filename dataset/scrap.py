
import requests
from bs4 import BeautifulSoup
import csv
import new

URL = "https://annauniv.irins.org/faculty/index/Department+of+Information+Science+and+Technology"
r = requests.get(URL)

soup = BeautifulSoup(r.content,"html5lib") # If this line causes an error, run 'pip install html5lib' or install html5lib
s=soup.find_all("div",class_="cbp-item")


def content_parser(req):
    pub=req.find("div",class_="panel-body border_box")
    print(pub)
    doc=pub.find_all("div",class_="row")



header = ['name', 'role', 'subject']
with open("details.csv", mode='a', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=header)


    writer.writeheader()
    
header2=["name","year","title","type"]
with open("books.csv", mode='a', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=header2)


    writer.writeheader()

for i in s:
    m={"name":i.find("h3").text , "role":i.find("span",class_="color-lightYellow").text,"subject":i.find("span",class_="color-lightWhite").text}
    with open("details.csv", mode='a', newline='') as file:
       
        writer = csv.DictWriter(file, fieldnames=header)
    
        writer.writerow(m)
    print(i.find('a',class_="btn-u btn-u-xs btn-u-sea mt10")["href"])
    d=new.client(i.find('a',class_="btn-u btn-u-xs btn-u-sea mt10")["href"])
    for j in d:
        s={"name":i.find("h3").text,"year":j[0],"title":j[2],"type":j[1]}
        with open("books.csv", mode='a', newline='') as file:
       
            writer = csv.DictWriter(file, fieldnames=header2)
        
            writer.writerow(s)
    

        

